import pandas as pd
import os
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import uuid
import config


# Helper: Convert DataFrame → Text Docs
def dataframe_to_docs(df: pd.DataFrame):
    docs = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        text_parts = []
        
        for key, value in row_dict.items():
            if pd.notna(value):
                if isinstance(value, dict):
                    # Handle nested dictionaries (like address)
                    nested_parts = [f"{k}: {v}" for k, v in value.items() if pd.notna(v)]
                    text_parts.append(f"{key}: {', '.join(nested_parts)}")
                else:
                    text_parts.append(f"{key}: {value}")
        
        docs.append(", ".join(text_parts))
    return docs



# Load property data from file (CSV or JSON)
def load_property_docs(file_path):
    _, ext = os.path.splitext(file_path.lower())
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")
    return dataframe_to_docs(df)



# Embeddings + Qdrant setup
embeddings = OpenAIEmbeddings(
    model=config.EMBEDDING_MODEL,
    openai_api_key=config.OPENAI_API_KEY,
)
qdrant = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)

print("✅ RAG system initialized. Ready to index uploaded data.")



# Create or connect to Qdrant collection
if config.COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
    print(f"🔄 Creating new collection: {config.COLLECTION_NAME}")
    qdrant.recreate_collection(
        collection_name=config.COLLECTION_NAME,
        vectors_config=VectorParams(size=config.EMBEDDING_DIM, distance=Distance.COSINE),
    )
    print("✅ Collection created. Use notebook or API to upload data.")


# Vectorstore and Retrieval setup
vectorstore = QdrantVectorStore(
    client=qdrant, collection_name=config.COLLECTION_NAME, embedding=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = OpenAI(
    model_name=config.LLM_MODEL,
    openai_api_key=config.OPENAI_API_KEY,
    temperature=0,
)

def qa_chain(query: str):
    """Custom QA function that retrieves relevant docs and asks LLM."""
    # Get relevant documents
    docs = retriever.invoke(query)
    
    # Create context from documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create prompt
    prompt = f"""You are a helpful assistant answering questions about property transactions. 
Analyze the property data provided below and give a direct, helpful answer.

Property Data:
{context}

Question: {query}

Instructions:
- If you can answer the question using the data above, provide a clear, specific answer
- If calculating averages, totals, or other statistics, show your work
- If the question asks about a specific year/time period not in the data, explain what years ARE available
- If the data is insufficient, be specific about what's missing (e.g., "No data found for year 2005")

Answer:"""
    
    # Get answer from LLM
    response = llm.invoke(prompt)
    
    # Extract text content from response
    if hasattr(response, 'content'):
        answer = response.content
    elif isinstance(response, str):
        answer = response
    else:
        answer = str(response)
    
    return {
        "result": answer,
        "source_documents": docs
    }



# Index Building Functions
def build_index_from_docs(docs):
    if not docs:
        print("⚠️ No documents provided for indexing.")
        return
    
    print(f"📝 Indexing {len(docs)} documents...")
    print(f"Sample doc: {docs[0][:100]}...")
    
    # Process in batches to avoid token limits
    batch_size = 50  # Process 50 documents at a time (faster!)
    total_batches = (len(docs) + batch_size - 1) // batch_size
    
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        print(f"  Processing batch {batch_num}/{total_batches} ({len(batch_docs)} docs)...")
        
        # Generate embeddings for this batch
        batch_embeddings = embeddings.embed_documents(batch_docs)
        
        # Store text in 'page_content' field for proper retrieval
        payload = [{"page_content": doc, "text": doc} for doc in batch_docs]
        ids = [str(uuid.uuid4()) for _ in batch_docs]
        
        # Upload this batch to Qdrant (with wait=True to ensure indexing completes)
        qdrant.upload_collection(
            config.COLLECTION_NAME, 
            batch_embeddings, 
            payload, 
            ids,
            wait=True  # Wait for indexing to complete
        )
    
    print(f"✅ Successfully indexed {len(docs)} documents!")


def build_index_from_df(df: pd.DataFrame):
    docs = dataframe_to_docs(df)
    build_index_from_docs(docs)


def build_index_from_file(file_path: str):
    docs = load_property_docs(file_path)
    build_index_from_docs(docs)

def clear_and_rebuild_collection():
    """Clear the collection and rebuild it from scratch."""
    print("🗑️ Clearing existing collection...")
    qdrant.delete_collection(config.COLLECTION_NAME)
    
    print("🔄 Recreating collection...")
    qdrant.recreate_collection(
        collection_name=config.COLLECTION_NAME,
        vectors_config=VectorParams(size=config.EMBEDDING_DIM, distance=Distance.COSINE),
    )
    
    print("✅ Collection cleared. Ready for new data to be indexed.")



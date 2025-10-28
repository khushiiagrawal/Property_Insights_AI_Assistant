# Property Insights AI Assistant - Architecture

## Overview
A RAG-based AI system for analyzing property transaction data using LangChain, Qdrant, and GPT-4.

## Core Components

### 1. **Data Ingestion** (`rag.ipynb`)
- **Purpose**: Interactive file upload and processing
- **Supports**: CSV and JSON files
- **Features**:
  - File upload widget
  - Automatic DataFrame conversion
  - Direct indexing into Qdrant
- **Usage**: Upload data dynamically without hardcoded paths

### 2. **RAG Pipeline** (`main.py`)
- **Purpose**: Core retrieval-augmented generation logic
- **Components**:
  - OpenAI Embeddings (text-embedding-ada-002)
  - Qdrant Vector Database
  - GPT-4 for answer generation
  - Custom QA chain with source attribution
- **Features**:
  - Dynamic document processing
  - Nested JSON support
  - Flexible indexing functions

### 3. **REST API** (`api.py`)
- **Purpose**: HTTP interface for the QA system
- **Endpoints**:
  - `GET /` - API documentation
  - `GET /health` - Health check
  - `POST /ask` - Ask questions about properties
- **Port**: 5001

### 4. **Configuration** (`config.py`)
- **Purpose**: Centralized environment-based configuration
- **Variables**:
  - `OPENAI_API_KEY` - OpenAI API key
  - `QDRANT_API_KEY` - Qdrant API key
  - `QDRANT_URL` - Qdrant instance URL
  - `EMBEDDING_MODEL` - Embedding model (default: text-embedding-ada-002)
  - `LLM_MODEL` - LLM model (default: gpt-4)
  - `COLLECTION_NAME` - Qdrant collection name
  - `EMBEDDING_DIM` - Embedding dimensions (default: 1536)

## Data Flow

```
1. Upload File (Notebook/API)
   ↓
2. Convert to DataFrame
   ↓
3. Transform to Text Documents
   ↓
4. Generate Embeddings (OpenAI)
   ↓
5. Store in Qdrant Vector DB
   ↓
6. User Query → Retrieve Relevant Docs
   ↓
7. Generate Answer (GPT-4 + Context)
   ↓
8. Return Answer + Sources
```

## Key Design Decisions

### ✅ Dynamic Data Loading
- **No hardcoded file paths**
- Data uploaded via notebook or API
- Supports any CSV/JSON structure with nested objects

### ✅ Flexible Indexing
- `build_index_from_df(df)` - From pandas DataFrame
- `build_index_from_file(path)` - From file path
- `build_index_from_docs(docs)` - From text documents

### ✅ Source Attribution
- Every answer includes source documents
- Transparency in data retrieval
- Easy verification of AI responses

### ✅ Environment-Based Config
- All sensitive data in `.env`
- Easy deployment across environments
- No secrets in code

## File Structure

```
Property_Insights_AI_Assistant/
├── main.py              # Core RAG pipeline
├── api.py               # Flask REST API
├── config.py            # Configuration management
├── rag.ipynb            # Interactive data upload
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── API_USAGE.md         # API documentation
├── ARCHITECTURE.md      # This file
└── temp/                # Temporary upload storage
```

## Usage Workflow

### Step 1: Setup Environment
```bash
# Create .env file
OPENAI_API_KEY=your_key_here
QDRANT_API_KEY=your_key_here
QDRANT_URL=your_qdrant_url_here
```

### Step 2: Upload Data
**Option A: Via Notebook**
1. Open `rag.ipynb`
2. Upload CSV/JSON file
3. Run indexing cell

**Option B: Via API**
(Future implementation)

### Step 3: Query Data
**Option A: Via API**
```bash
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What properties are available?"}'
```

**Option B: Via Notebook**
(Import qa_chain and use directly)

## Quality Improvements

### Removed Hardcoded Dependencies
- ❌ No `CSV_PATH` environment variable
- ❌ No default data file loading
- ❌ No hardcoded column names
- ✅ Pure dynamic data processing

### Improved Prompt Engineering
- Clear instructions for LLM
- Explicit context handling
- Better error messages

### Better Document Processing
- Handles nested JSON objects
- Flexible DataFrame conversion
- Proper null value handling

## Dependencies

- **LangChain**: RAG framework
- **OpenAI**: Embeddings and LLM
- **Qdrant**: Vector database
- **Flask**: REST API
- **Pandas**: Data processing
- **ipywidgets**: Notebook file upload

## Environment Requirements

- Python 3.8+
- OpenAI API access
- Qdrant instance (cloud or local)
- Internet connection for API calls


import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "property_insights")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 1536))
CSV_PATH = os.getenv("CSV_PATH", "data.json")

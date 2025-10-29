import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None  # None for local Docker, string for Qdrant Cloud
QDRANT_URL = os.getenv("QDRANT_URL", "https://3ad12283-4bb5-4665-b891-caadab24a1e2.eu-central-1-0.aws.cloud.qdrant.io")  # Default to local Docker
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "property_insights")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 1536))

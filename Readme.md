# 🏠 Property Insights AI Assistant

A **Retrieval-Augmented Generation (RAG)** system that answers natural language queries about property transactions using **LangChain**, **Qdrant Cloud**, and **GPT-4**.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://www.langchain.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-purple.svg)](https://cloud.qdrant.io/)
[![Flask](https://img.shields.io/badge/Flask-3.1-red.svg)](https://flask.palletsprojects.com/)

---

## ✨ Features

- 📊 **Dynamic Data Upload** - Upload CSV/JSON files via Jupyter notebook
- 🔍 **Vector Search** - Qdrant Cloud for fast similarity search
- 🤖 **GPT-4 Powered** - Intelligent answers with source attribution
- 🚀 **REST API** - Flask-based endpoints for easy integration
- 🎯 **Batch Processing** - Handles large datasets efficiently
- 🔐 **Secure** - Environment-based configuration
- 📝 **Well Documented** - Comprehensive guides and examples

---

## 🏗️ Architecture

```
User Upload (Jupyter) → Data Processing → OpenAI Embeddings
                                              ↓
                                         Qdrant Cloud
                                         (Vector DB)
                                              ↓
    User Query → Flask API → Vector Search → GPT-4 → Answer
```

---

## 💻 Quick Start

### 1. **Clone & Setup**

```bash
git clone <your-repo-url>
cd Property_Insights_AI_Assistant
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **Configure Environment**

Create `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key

# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key

# Model Configuration
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-4o-mini
COLLECTION_NAME=property_insights
EMBEDDING_DIM=1536
```

**Get Qdrant Cloud credentials:** https://cloud.qdrant.io/ (Free 1GB tier)

### 3. **Upload Data (Jupyter Notebook)**

```bash
jupyter notebook rag.ipynb
```

- **Cell 1:** Upload CSV/JSON file
- **Cell 3:** Index into Qdrant (auto-clears old data)

### 4. **Start API**

```bash
python api.py
```

API runs on `http://localhost:5001`

### 5. **Test Queries**

```bash
# Health check
curl http://localhost:5001/health

# Ask a question
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the average property price in Pune?"}'
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation |
| `/health` | GET | Health check |
| `/ask` | POST | Query the AI system |

**Example Request:**
```json
{
  "question": "What is the average property price in Mumbai?"
}
```

---

## 📂 Project Structure

```
Property_Insights_AI_Assistant/
├── main.py              # Core RAG pipeline
├── api.py               # Flask REST API
├── config.py            # Configuration
├── rag.ipynb            # Interactive notebook
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (create this)
├── .gitignore           # Security exclusions       
│
└── temp/                # Temporary uploads
```

---



## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.13 |
| **Framework** | LangChain |
| **Vector DB** | Qdrant Cloud |
| **LLM** | GPT-4 (gpt-4o-mini) |
| **Embeddings** | OpenAI text-embedding-ada-002 |
| **API** | Flask 3.1 |
| **Data** | Pandas, JSON/CSV |
| **Notebook** | Jupyter |

---



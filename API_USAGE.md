# Property Insights AI Assistant API

A simple Flask API for querying property data using RAG (Retrieval-Augmented Generation).

## Quick Start

1. **Start the API:**
   ```bash
   python api.py
   ```

2. **Test the API:**
   ```bash
   # Check if API is running
   curl http://localhost:5001/health
   
   # Ask a question
   curl -X POST http://localhost:5001/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What properties are available?"}'
   ```

## API Endpoints

### GET `/`
- **Description:** API documentation and usage info
- **Response:** JSON with available endpoints and examples

### GET `/health`
- **Description:** Health check
- **Response:** 
  ```json
  {
    "status": "healthy",
    "message": "Property Insights AI Assistant is running"
  }
  ```

### POST `/ask`
- **Description:** Ask questions about property data
- **Body:** 
  ```json
  {
    "question": "What is the average price of Single Family Homes?"
  }
  ```
- **Response:**
  ```json
  {
    "question": "What is the average price of Single Family Homes?",
    "answer": "Based on the available data...",
    "sources": ["property data 1", "property data 2"],
    "sources_count": 2
  }
  ```

## Example Questions

- "What properties are available?"
- "What is the average price of Single Family Homes?"
- "Show me properties in California"
- "What's the most expensive property?"
- "How many bedrooms does the property on Main St have?"

## Error Handling

- **400 Bad Request:** Missing question in JSON body
- **500 Internal Server Error:** Server-side processing error

## Requirements

- Python 3.8+
- Flask
- OpenAI API key
- Qdrant vector database
- All dependencies from `requirements.txt`

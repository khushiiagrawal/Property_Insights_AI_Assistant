from flask import Flask, request, jsonify
from main import qa_chain

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Property Insights AI Assistant API",
        "version": "1.0",
        "endpoints": {
            "/ask": "POST - Ask questions about properties",
            "/health": "GET - Check API health"
        },
        "usage": {
            "ask_question": {
                "method": "POST",
                "url": "/ask",
                "body": {"question": "What properties are available?"}
            }
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Property Insights AI Assistant is running"
    })

@app.route('/ask', methods=['POST'])
def ask():
    """
    Ask questions about property data.
    
    Expected JSON body:
    {
        "question": "What is the average price of Single Family Homes?"
    }
    """
    try:
        payload = request.get_json(force=True, silent=True) or {}
        user_query = payload.get('question') or payload.get('query')
        
        if not user_query:
            return jsonify({
                "error": "Missing 'question' or 'query' in JSON body",
                "example": {"question": "What properties are available?"}
            }), 400
        
        # Get answer from QA chain
        result = qa_chain(user_query)
        
        return jsonify({
            "question": user_query,
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]],
            "sources_count": len(result["source_documents"])
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    print("🏠 Starting Property Insights AI Assistant API...")
    print("📡 API will be available at: http://localhost:5001")
    print("📖 Documentation at: http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)



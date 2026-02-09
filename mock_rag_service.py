#!/usr/bin/env python3
"""
Mock RAG Service for Testing

A simple mock RAG service that responds to queries with generated responses.
This is useful for testing the Video Transcoder RAG integration without
needing a full RAG service setup.

Usage:
    python mock_rag_service.py

Then configure your Video Transcoder .env:
    RAG_URL=localhost
    RAG_PORT=8000
    RAG_ENDPOINT=/api/query
"""

from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

# Sample responses for different query types
SAMPLE_RESPONSES = {
    'yoga': "Okay, let's design a 75-minute YogaBharati-inspired class focusing on breath, alignment, and mindful movement. We'll start with centering and pranayama, move through sun salutations, work on standing poses for strength and balance, incorporate seated poses for flexibility, and end with deep relaxation.",
    'quantum': "Quantum computing leverages quantum mechanical phenomena like superposition and entanglement to perform computations. Unlike classical bits that are either 0 or 1, quantum bits (qubits) can exist in multiple states simultaneously, enabling parallel processing of information.",
    'machine learning': "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions based on those patterns.",
    'default': "I understand your query. Based on the information available, here's a comprehensive response addressing your question. This mock service demonstrates the RAG integration functionality."
}

def get_sample_response(query):
    """Generate a sample response based on query content"""
    query_lower = query.lower()
    
    for keyword, response in SAMPLE_RESPONSES.items():
        if keyword in query_lower:
            return response
    
    return SAMPLE_RESPONSES['default']

@app.route('/api/query', methods=['POST'])
def query():
    """Handle RAG query requests"""
    try:
        data = request.json
        
        # Validate request
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Query is required'
            }), 400
        
        query_text = data.get('query', '')
        top_k = data.get('top_k', 3)
        use_rag = data.get('use_rag', True)
        temperature = data.get('temperature', 0.1)
        
        # Log request
        print(f"Received query: {query_text}")
        print(f"Parameters: top_k={top_k}, use_rag={use_rag}, temperature={temperature}")
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))
        
        # Generate response
        answer = get_sample_response(query_text)
        
        # Add some variation based on parameters
        if not use_rag:
            answer = f"[Without RAG] {answer}"
        
        response_data = {
            'answer': answer,
            'sources': None if not use_rag else ['document_1.pdf', 'document_2.pdf', 'document_3.pdf'][:top_k],
            'query': query_text
        }
        
        print(f"Sending response: {len(answer)} characters")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Mock RAG Service',
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with service info"""
    return jsonify({
        'service': 'Mock RAG Service',
        'version': '1.0.0',
        'endpoints': {
            'query': '/api/query (POST)',
            'health': '/health (GET)'
        },
        'example_request': {
            'query': 'Generate Yoga Class',
            'top_k': 3,
            'use_rag': True,
            'temperature': 0.1
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Mock RAG Service Starting...")
    print("=" * 60)
    print()
    print("Service will be available at: http://localhost:8000")
    print("Query endpoint: http://localhost:8000/api/query")
    print("Health check: http://localhost:8000/health")
    print()
    print("Configure Video Transcoder .env:")
    print("  RAG_URL=localhost")
    print("  RAG_PORT=8000")
    print("  RAG_ENDPOINT=/api/query")
    print()
    print("Test with:")
    print("  curl -X POST http://localhost:8000/api/query \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"query\":\"test\",\"top_k\":3,\"use_rag\":true,\"temperature\":0.1}'")
    print()
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)

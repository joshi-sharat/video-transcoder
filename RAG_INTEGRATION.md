# 🤖 RAG Service Integration

## Overview

The Video Transcoder now includes a **RAG (Retrieval Augmented Generation)** query interface that allows you to connect to an external RAG service and submit queries.

## Features

- 🔌 **Configurable RAG Service Connection** - Set custom URL and port
- 📊 **Query Parameters** - Control top_k, temperature, and RAG usage
- 🎨 **Modern UI** - Clean, responsive interface for submitting queries
- 🔄 **RESTful API** - Programmatic access via `/api/rag/query`
- ⚡ **Real-time Responses** - See RAG responses immediately
- 🛡️ **Error Handling** - Clear error messages for connection issues

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# RAG Service Configuration
RAG_URL=localhost
RAG_PORT=8000
RAG_ENDPOINT=/api/query

# Default RAG parameters
RAG_DEFAULT_TOP_K=3
RAG_DEFAULT_TEMPERATURE=0.1
```

### Example Configurations

**Local RAG Service:**
```env
RAG_URL=localhost
RAG_PORT=8000
RAG_ENDPOINT=/api/query
```

**Remote RAG Service:**
```env
RAG_URL=192.168.1.100
RAG_PORT=5000
RAG_ENDPOINT=/query
```

**Cloud RAG Service:**
```env
RAG_URL=rag-service.example.com
RAG_PORT=443
RAG_ENDPOINT=/api/v1/query
```

## Usage

### Web Interface

1. **Navigate to RAG Interface:**
   - Open http://localhost:5000
   - Click "🤖 RAG Query" in the header
   - Or go directly to: http://localhost:5000/rag

2. **Submit a Query:**
   - Enter your query in the text area
   - Adjust parameters (top_k, temperature, use_rag)
   - Click "Submit Query"
   - View the response

### API Endpoint

**Endpoint:** `POST /api/rag/query`

**Request Body:**
```json
{
    "query": "Generate Yoga Class",
    "top_k": 3,
    "use_rag": true,
    "temperature": 0.1
}
```

**Response (Success):**
```json
{
    "answer": "Okay, let's design a 75-minute YogaBharati-inspired class ...",
    "sources": null,
    "query": "Generate Yoga Class"
}
```

**Response (Error):**
```json
{
    "error": "Cannot connect to RAG service",
    "details": "Unable to reach http://localhost:8000/api/query. Make sure the RAG service is running."
}
```

### cURL Examples

**Basic Query:**
```bash
curl -X POST http://localhost:5000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate Yoga Class",
    "top_k": 3,
    "use_rag": true,
    "temperature": 0.1
  }'
```

**With Custom Parameters:**
```bash
curl -X POST http://localhost:5000/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain machine learning",
    "top_k": 5,
    "use_rag": false,
    "temperature": 0.7
  }'
```

### Python Example

```python
import requests

url = "http://localhost:5000/api/rag/query"
payload = {
    "query": "Generate Yoga Class",
    "top_k": 3,
    "use_rag": True,
    "temperature": 0.1
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Answer: {data['answer']}")
print(f"Query: {data['query']}")
print(f"Sources: {data['sources']}")
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:5000/api/rag/query', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: 'Generate Yoga Class',
        top_k: 3,
        use_rag: true,
        temperature: 0.1
    })
});

const data = await response.json();
console.log('Answer:', data.answer);
```

## Parameters

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | *required* | The question or prompt to send to RAG service |
| `top_k` | integer | 3 | Number of relevant documents to retrieve |
| `use_rag` | boolean | true | Whether to use RAG or just LLM |
| `temperature` | float | 0.1 | LLM temperature (0.0-2.0), lower = more focused |

## Error Codes

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | Bad Request | Missing or invalid query parameter |
| 503 | Service Unavailable | Cannot connect to RAG service |
| 504 | Gateway Timeout | RAG service took too long to respond |
| 500 | Internal Server Error | Unexpected error occurred |

## Troubleshooting

### Error: "Cannot connect to RAG service"

**Problem:** The application cannot reach your RAG service.

**Solutions:**
1. **Check if RAG service is running:**
   ```bash
   curl http://localhost:8000/api/query
   ```

2. **Verify .env configuration:**
   ```env
   RAG_URL=localhost  # Check this matches your RAG service
   RAG_PORT=8000      # Check port is correct
   ```

3. **Check firewall settings:**
   - Make sure the port is not blocked
   - For remote services, ensure network access

4. **Test RAG service directly:**
   ```bash
   curl -X POST http://localhost:8000/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "top_k": 3, "use_rag": true, "temperature": 0.1}'
   ```

### Error: "RAG service timeout"

**Problem:** The RAG service is taking too long to respond.

**Solutions:**
1. Check RAG service performance
2. Reduce `top_k` value
3. Simplify your query
4. Check network latency

### Error: "RAG service error"

**Problem:** The RAG service returned an error.

**Solutions:**
1. Check RAG service logs
2. Verify request format matches RAG service expectations
3. Ensure RAG service is properly configured

## Setting Up a Test RAG Service

If you don't have a RAG service, here's a simple mock server for testing:

**mock_rag_server.py:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    query = data.get('query', '')
    
    # Mock response
    return jsonify({
        'answer': f'Mock response for: {query}',
        'sources': None,
        'query': query
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Run it:**
```bash
python mock_rag_server.py
```

Then update your `.env`:
```env
RAG_URL=localhost
RAG_PORT=8000
RAG_ENDPOINT=/api/query
```

## Integration with Existing Code

The RAG integration follows the existing codebase conventions:

- **Configuration:** Uses `app/config.py` pattern
- **Routes:** Added to `app.py` following Flask conventions
- **UI:** Uses same CSS framework as main interface
- **Error Handling:** Consistent error response format
- **Environment:** Configured via `.env` file

## API Response Format

### Success Response

```json
{
    "answer": "The generated response from RAG service",
    "sources": ["source1", "source2"] or null,
    "query": "The original query text"
}
```

### Error Response

```json
{
    "error": "Error type",
    "details": "Detailed error message"
}
```

## Security Considerations

1. **Input Validation:** Queries are validated before sending to RAG service
2. **Timeout Protection:** 30-second timeout prevents hanging requests
3. **Error Sanitization:** Error messages don't expose sensitive information
4. **CORS:** Uses existing CORS configuration

## Future Enhancements

Potential improvements:

- [ ] Query history and saved queries
- [ ] Response caching
- [ ] Multiple RAG service support
- [ ] Streaming responses
- [ ] Authentication for RAG service
- [ ] Query templates
- [ ] Export responses to file

## Support

For issues or questions:
1. Check the logs in the console
2. Verify RAG service is accessible
3. Review error messages in the UI
4. Check network connectivity

---

**RAG Integration Version:** 1.0.0  
**Compatible with:** Video Transcoder v1.0+

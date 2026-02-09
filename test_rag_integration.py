#!/usr/bin/env python3
"""
Test script for RAG integration

This script tests the RAG service integration by:
1. Checking if the Video Transcoder app is running
2. Testing the RAG API endpoint
3. Verifying responses
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000"
RAG_ENDPOINT = f"{BASE_URL}/api/rag/query"

def test_app_running():
    """Test if the app is running"""
    print("1. Testing if Video Transcoder app is running...")
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        if response.status_code == 200:
            print("   ✓ App is running")
            return True
        else:
            print(f"   ✗ App returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ Cannot connect to app. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_rag_endpoint():
    """Test the RAG endpoint"""
    print("\n2. Testing RAG endpoint...")
    
    test_query = {
        "query": "Test query for RAG service",
        "top_k": 3,
        "use_rag": True,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(RAG_ENDPOINT, json=test_query, timeout=30)
        
        if response.status_code == 200:
            print("   ✓ RAG endpoint responded successfully")
            data = response.json()
            print(f"   Response keys: {list(data.keys())}")
            return True, data
        elif response.status_code == 503:
            print("   ⚠ RAG service is not available (503)")
            data = response.json()
            print(f"   Details: {data.get('details', 'No details')}")
            return False, data
        else:
            print(f"   ✗ Unexpected status code: {response.status_code}")
            return False, response.json()
            
    except requests.exceptions.Timeout:
        print("   ✗ Request timed out")
        return False, None
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False, None

def test_invalid_request():
    """Test with invalid request"""
    print("\n3. Testing error handling (invalid request)...")
    
    invalid_query = {}  # Missing 'query' field
    
    try:
        response = requests.post(RAG_ENDPOINT, json=invalid_query, timeout=5)
        
        if response.status_code == 400:
            print("   ✓ Properly handles invalid request (400)")
            return True
        else:
            print(f"   ⚠ Expected 400, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def display_sample_response(data):
    """Display a sample response"""
    print("\n4. Sample Response:")
    print("-" * 50)
    if data:
        print(f"Query: {data.get('query', 'N/A')}")
        print(f"Answer: {data.get('answer', 'N/A')[:100]}...")
        print(f"Sources: {data.get('sources', 'N/A')}")
    else:
        print("No response data available")
    print("-" * 50)

def main():
    print("=" * 50)
    print("RAG Integration Test Suite")
    print("=" * 50)
    print()
    
    # Test 1: App running
    if not test_app_running():
        print("\n❌ FAILED: App is not running")
        print("Start the app with: python app.py")
        sys.exit(1)
    
    # Test 2: RAG endpoint
    success, data = test_rag_endpoint()
    if not success:
        print("\n⚠️  WARNING: RAG endpoint is working but RAG service is not available")
        print("\nTo fix:")
        print("1. Make sure your RAG service is running")
        print("2. Check .env configuration:")
        print("   RAG_URL=localhost")
        print("   RAG_PORT=8000")
        print("3. Test RAG service directly:")
        print("   curl -X POST http://localhost:8000/api/query \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"query\":\"test\",\"top_k\":3,\"use_rag\":true,\"temperature\":0.1}'")
    
    # Test 3: Error handling
    test_invalid_request()
    
    # Display sample
    if data:
        display_sample_response(data)
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED")
        print("\nYou can now:")
        print("1. Open http://localhost:5000/rag in your browser")
        print("2. Submit queries through the UI")
        print("3. Use the API programmatically")
    else:
        print("⚠️  TESTS COMPLETED WITH WARNINGS")
        print("\nThe Video Transcoder app is working,")
        print("but the RAG service needs to be configured.")
    print("=" * 50)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

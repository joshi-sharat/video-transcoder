#!/bin/bash

# Video Transcoder API Testing Script

API_BASE="http://localhost:5000/api"

echo "🧪 Video Transcoder API Test Suite"
echo "=================================="
echo ""

# Test 1: Get system status
echo "1️⃣ Testing GET /api/status"
curl -s "$API_BASE/status" | python3 -m json.tool
echo ""
echo ""

# Test 2: Get current settings
echo "2️⃣ Testing GET /api/settings"
curl -s "$API_BASE/settings" | python3 -m json.tool
echo ""
echo ""

# Test 3: Update settings
echo "3️⃣ Testing POST /api/settings"
curl -s -X POST "$API_BASE/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "source_folder": "/tmp/videos/source",
    "output_folder": "/tmp/videos/output",
    "watch_enabled": false,
    "output_format": "mp4",
    "video_codec": "libx264",
    "audio_codec": "aac",
    "preset": "medium",
    "crf": 23
  }' | python3 -m json.tool
echo ""
echo ""

# Test 4: Get all jobs
echo "4️⃣ Testing GET /api/jobs"
curl -s "$API_BASE/jobs" | python3 -m json.tool
echo ""
echo ""

# Test 5: Get completed jobs only
echo "5️⃣ Testing GET /api/jobs?status=completed"
curl -s "$API_BASE/jobs?status=completed" | python3 -m json.tool
echo ""
echo ""

# Test 6: Scan for new videos
echo "6️⃣ Testing POST /api/scan"
curl -s -X POST "$API_BASE/scan" | python3 -m json.tool
echo ""
echo ""

echo "✅ API tests completed!"

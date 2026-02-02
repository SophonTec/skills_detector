#!/bin/bash
set -e

echo "🧪 Testing AI Skills Tracker..."
echo ""

API_URL="${API_URL:-http://localhost}"

echo "1. Testing health endpoint..."
curl -s "${API_URL}/api/v1/health" | jq .

echo ""
echo "2. Testing stats endpoint..."
curl -s "${API_URL}/api/v1/stats" | jq .

echo ""
echo "3. Testing skills endpoint (latest)..."
curl -s "${API_URL}/api/v1/skills?sort=latest&limit=5" | jq '.skills[0]'

echo ""
echo "4. Testing skills endpoint (hot)..."
curl -s "${API_URL}/api/v1/skills?sort=hot&limit=5" | jq '.skills[0]'

echo ""
echo "5. Testing skills endpoint (used)..."
curl -s "${API_URL}/api/v1/skills?sort=used&limit=5" | jq '.skills[0]'

echo ""
echo "6. Testing GitHub source filter..."
curl -s "${API_URL}/api/v1/skills?source=github&limit=3" | jq '.skills[].source'

echo ""
echo "7. Testing npm source filter..."
curl -s "${API_URL}/api/v1/skills?source=npm&limit=3" | jq '.skills[].source'

echo ""
echo "8. Testing scrapes endpoint..."
curl -s "${API_URL}/api/v1/scrapes?limit=5" | jq .

echo ""
echo "✅ All tests completed!"

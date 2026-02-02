#!/bin/bash
echo "🛑 Stopping AI Skills Tracker..."

kill $(ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}') 2>/dev/null
kill $(ps aux | grep "next dev" | grep -v grep | awk '{print $2}') 2>/dev/null

sleep 2

echo "✅ Services stopped!"
echo ""
echo "To restart:"
echo "  cd /Users/sophon/workspace/skill_detector/backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "  cd /Users/sophon/workspace/skill_detector/frontend"
echo "  npm run dev"

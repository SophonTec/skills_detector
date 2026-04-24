#!/bin/bash
set -e

cd /Users/sophon/workspace/skill_detector/backend

export DATABASE_PATH=/tmp/skills.db
export DATABASE_ENCRYPTION_KEY=G0aMjDv9MaAJPY5iBiBILR-l4sQxTifk
export SECRET_KEY=FPUGa-UGVANpe_m4ULlVG46e9y9VJE_5WK2QXNQWecM
export FRONTEND_URL=http://localhost:3000

echo "Starting backend..."

source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

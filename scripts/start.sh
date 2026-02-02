#!/bin/bash
set -e

echo "🚀 Starting AI Skills Tracker..."

if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running!"
    exit 1
fi

echo "📦 Building Docker images..."
docker compose build

echo "🔄 Starting services..."
docker compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

echo "✅ Services started!"
echo ""
echo "📊 Access the application at: http://localhost"
echo "📖 API documentation: http://localhost/api/v1/docs"
echo ""
echo "📝 View logs with: docker compose logs -f"
echo "🛑 Stop services with: docker compose down"

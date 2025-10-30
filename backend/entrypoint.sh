#!/bin/bash
set -e

echo "⏳ Waiting for database to start..."
sleep 5

echo "🗄️  Creating database tables..."
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

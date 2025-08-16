#!/bin/bash

# Development setup script

set -e

echo "🛠️  Setting up development environment"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment"
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment"
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "📦 Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template"
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running. Please start PostgreSQL server."
    echo "   You can use Docker: docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15"
fi

# Check if Redis is running
if ! redis-cli ping >/dev/null 2>&1; then
    echo "⚠️  Redis is not running. Please start Redis server."
    echo "   You can use Docker: docker run -d --name redis -p 6379:6379 redis:7-alpine"
fi

echo "✅ Development environment setup complete!"
echo "🚀 To start the development server:"
echo "   source venv/bin/activate  # or venv/Scripts/activate on Windows"
echo "   python main.py"

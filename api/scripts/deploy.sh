#!/bin/bash

# Deployment script for Stock Market Data Warehouse API

set -e

echo "🚀 Starting deployment of Stock Market Data Warehouse API"

# Check if required tools are installed
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template"
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration before running again"
    exit 1
fi

# Build and start services
echo "🏗️  Building Docker images"
docker-compose build

echo "🗄️  Starting database and cache services"
docker-compose up -d db redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready"
sleep 10

# Run database migrations/setup
echo "🗃️  Setting up database"
docker-compose run --rm api python -c "from app.db import create_tables; create_tables()"

# Start all services
echo "🌟 Starting all services"
docker-compose up -d

# Wait for API to be ready
echo "⏳ Waiting for API to be ready"
sleep 15

# Health check
echo "🏥 Performing health check"
if curl -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo "✅ API is healthy and ready!"
    echo "📋 API Documentation: http://localhost:8000/docs"
    echo "🔍 Health Check: http://localhost:8000/api/v1/health"
    echo "📊 Metrics: http://localhost:8000/api/v1/metrics"
    echo "📈 Grafana: http://localhost:3000 (admin/admin)"
    echo "🎯 Prometheus: http://localhost:9090"
else
    echo "❌ API health check failed"
    echo "📋 Checking logs:"
    docker-compose logs api
    exit 1
fi

echo "🎉 Deployment completed successfully!"

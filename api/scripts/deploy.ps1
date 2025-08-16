# PowerShell deployment script for Windows

Write-Host "🚀 Starting deployment of Stock Market Data Warehouse API" -ForegroundColor Green

# Check if required tools are installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "📄 Creating .env file from template" -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please update .env file with your configuration before running again" -ForegroundColor Yellow
    exit 1
}

# Build and start services
Write-Host "🏗️  Building Docker images" -ForegroundColor Blue
docker-compose build

Write-Host "🗄️  Starting database and cache services" -ForegroundColor Blue
docker-compose up -d db redis

# Wait for database to be ready
Write-Host "⏳ Waiting for database to be ready" -ForegroundColor Yellow
Start-Sleep 10

# Run database migrations/setup
Write-Host "🗃️  Setting up database" -ForegroundColor Blue
docker-compose run --rm api python -c "from app.db import create_tables; create_tables()"

# Start all services
Write-Host "🌟 Starting all services" -ForegroundColor Blue
docker-compose up -d

# Wait for API to be ready
Write-Host "⏳ Waiting for API to be ready" -ForegroundColor Yellow
Start-Sleep 15

# Health check
Write-Host "🏥 Performing health check" -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API is healthy and ready!" -ForegroundColor Green
        Write-Host "📋 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "🔍 Health Check: http://localhost:8000/api/v1/health" -ForegroundColor Cyan
        Write-Host "📊 Metrics: http://localhost:8000/api/v1/metrics" -ForegroundColor Cyan
        Write-Host "📈 Grafana: http://localhost:3000 (admin/admin)" -ForegroundColor Cyan
        Write-Host "🎯 Prometheus: http://localhost:9090" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ API health check failed" -ForegroundColor Red
    Write-Host "📋 Checking logs:" -ForegroundColor Yellow
    docker-compose logs api
    exit 1
}

Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green

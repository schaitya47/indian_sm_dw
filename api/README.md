# Stock Market Data Warehouse API

A robust, scalable REST API for accessing stock market data warehouse with comprehensive features for enterprise-level deployment.

## Features

- **High Performance**: FastAPI with async/await support
- **Scalable Architecture**: Microservices-ready design
- **Caching**: Redis-based caching for optimal performance
- **Authentication**: JWT-based security with role-based access control
- **Rate Limiting**: API throttling to prevent abuse
- **Monitoring**: Prometheus metrics and structured logging
- **Database**: PostgreSQL with connection pooling
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Testing**: Comprehensive test suite
- **Docker Ready**: Containerized deployment

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis 6+

### Installation

1. Clone and navigate to the API directory:
```bash
cd api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

### Docker
```bash
docker build -t stock-api .
docker run -p 8000:8000 stock-api
```

### Production
For production deployment, use a process manager like systemd or deployment to Kubernetes.

## Architecture

```
api/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── core/          # Core configuration and security
│   ├── db/            # Database models and connection
│   ├── services/      # Business logic services
│   ├── schemas/       # Pydantic models
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── docker/            # Docker configuration
└── scripts/           # Deployment scripts
```

## Performance Features

- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Optimized SQL queries with proper indexing
- **Caching Strategy**: Multi-level caching (Redis + in-memory)
- **Pagination**: Cursor-based pagination for large datasets
- **Async Processing**: Non-blocking I/O operations
- **Background Tasks**: Celery for heavy computations

## Security

- JWT authentication with refresh tokens
- API key authentication for service-to-service communication
- Rate limiting per user/IP
- Input validation and sanitization
- CORS configuration
- SQL injection protection

## Monitoring

- Prometheus metrics endpoint (`/metrics`)
- Structured logging with correlation IDs
- Health check endpoints
- Performance monitoring dashboards

"""
FastAPI application factory and configuration.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import api_router
from app.utils import metrics, check_rate_limit
from app.db import create_tables

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOGGING_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up Stock Market Data Warehouse API")
    
    # Create database tables if they don't exist
    try:
        create_tables()
        logger.info("Database tables verified/created")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Stock Market Data Warehouse API")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="""
        ## Stock Market Data Warehouse API

        A robust, scalable REST API for accessing comprehensive stock market data from the Indian market.

        ### Features
        - **Real-time and Historical Data**: Access OHLCV data, financial statements, and key ratios
        - **Advanced Filtering**: Filter by date ranges, sources, industries, and more
        - **Performance Optimized**: Redis caching, connection pooling, and optimized queries
        - **Rate Limited**: Built-in rate limiting to ensure fair usage
        - **Monitoring**: Prometheus metrics and health checks
        - **Pagination**: Cursor-based pagination for large datasets

        ### Data Sources
        - **NSE**: National Stock Exchange of India
        - **Yahoo Finance**: Global financial data
        - **TickerTape**: Financial ratios and fundamentals

        ### Authentication
        Currently open access. API key authentication available for higher rate limits.
        """,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Trusted host middleware for production
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure this properly in production
        )

    # Request timing and rate limiting middleware
    @app.middleware("http")
    async def add_process_time_and_rate_limit(request: Request, call_next):
        # Rate limiting
        if settings.RATE_LIMIT_ENABLED:
            try:
                rate_limit_headers = check_rate_limit(request)
                # Store headers to add to response
                request.state.rate_limit_headers = rate_limit_headers
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": e.detail},
                    headers=e.headers
                )
        
        # Request timing
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Add timing header
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Add rate limit headers
        if hasattr(request.state, "rate_limit_headers"):
            for key, value in request.state.rate_limit_headers.items():
                response.headers[key] = str(value)
        
        # Record metrics
        if settings.PROMETHEUS_ENABLED:
            try:
                endpoint = request.url.path
                method = request.method
                status_code = response.status_code
                metrics.record_request(method, endpoint, status_code, process_time)
            except Exception as e:
                logger.error(f"Error recording metrics: {e}")
        
        return response

    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url)
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "detail": exc.errors(),
                "path": str(request.url)
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected error occurred" if not settings.DEBUG else str(exc),
                "path": str(request.url)
            }
        )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Stock Market Data Warehouse API",
            "version": settings.PROJECT_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
            "health": f"{settings.API_V1_STR}/health",
            "metrics": f"{settings.API_V1_STR}/metrics"
        }

    return app


# Create application instance
app = create_application()

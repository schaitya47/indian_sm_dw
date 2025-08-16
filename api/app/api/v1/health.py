"""
Health check and system monitoring endpoints.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from app.utils import get_health_status, get_detailed_health, get_metrics
from app.schemas import HealthCheck
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Get basic health status of the API service.
    
    Returns:
    - Service status (healthy/unhealthy/degraded)
    - Timestamp
    - API version
    - Database status
    - Cache status
    """
    return get_health_status()


@router.get("/health/detailed")
async def detailed_health_check():
    """
    Get detailed health information including system metrics.
    
    Returns comprehensive health data including:
    - All basic health information
    - Database version and connection pool status
    - Cache statistics
    - System resource usage
    - Process information
    """
    return get_detailed_health()


@router.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics():
    """
    Get Prometheus metrics in text format.
    
    Returns metrics for:
    - HTTP request counts and durations
    - Database query performance
    - Cache hit/miss rates
    - System resource usage
    - Application-specific metrics
    """
    return get_metrics()


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for load balancer health checks.
    
    Returns a simple "pong" response to verify the service is responding.
    """
    return {"status": "pong", "message": "API is running"}

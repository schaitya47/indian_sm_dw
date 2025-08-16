"""
Monitoring utilities for metrics and health checks.
"""

import time
import psutil
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy import text
from app.core.config import settings
from app.db.database import engine
from app.utils.cache import cache
import logging

logger = logging.getLogger(__name__)

# Prometheus metrics
if settings.PROMETHEUS_ENABLED:
    # Request metrics
    request_count = Counter(
        'http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status_code']
    )
    
    request_duration = Histogram(
        'http_request_duration_seconds',
        'HTTP request duration',
        ['method', 'endpoint']
    )
    
    # Database metrics
    db_connection_pool_size = Gauge(
        'db_connection_pool_size',
        'Database connection pool size'
    )
    
    db_connection_pool_checked_out = Gauge(
        'db_connection_pool_checked_out',
        'Database connections checked out'
    )
    
    db_query_duration = Histogram(
        'db_query_duration_seconds',
        'Database query duration',
        ['query_type']
    )
    
    # Cache metrics
    cache_hits = Counter('cache_hits_total', 'Total cache hits')
    cache_misses = Counter('cache_misses_total', 'Total cache misses')
    
    # System metrics
    system_memory_usage = Gauge('system_memory_usage_bytes', 'System memory usage')
    system_cpu_usage = Gauge('system_cpu_usage_percent', 'System CPU usage')


class MetricsCollector:
    """Collector for application metrics."""
    
    def __init__(self):
        self.enabled = settings.PROMETHEUS_ENABLED
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics."""
        if not self.enabled:
            return
        
        request_count.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_db_query(self, query_type: str, duration: float):
        """Record database query metrics."""
        if not self.enabled:
            return
        
        db_query_duration.labels(query_type=query_type).observe(duration)
    
    def record_cache_hit(self):
        """Record cache hit."""
        if not self.enabled:
            return
        
        cache_hits.inc()
    
    def record_cache_miss(self):
        """Record cache miss."""
        if not self.enabled:
            return
        
        cache_misses.inc()
    
    def update_system_metrics(self):
        """Update system resource metrics."""
        if not self.enabled:
            return
        
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            system_memory_usage.set(memory.used)
            
            # CPU usage
            cpu_percent = psutil.cpu_percent()
            system_cpu_usage.set(cpu_percent)
            
            # Database connection pool
            pool = engine.pool
            db_connection_pool_size.set(pool.size())
            db_connection_pool_checked_out.set(pool.checkedout())
            
        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")


# Global metrics collector
metrics = MetricsCollector()


def get_metrics() -> str:
    """Get Prometheus metrics in text format."""
    if not settings.PROMETHEUS_ENABLED:
        return "Metrics disabled"
    
    # Update system metrics before returning
    metrics.update_system_metrics()
    return generate_latest()


def get_health_status() -> Dict[str, Any]:
    """Get application health status."""
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }
    
    # Check database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health["database"] = "healthy"
    except Exception as e:
        health["database"] = f"unhealthy: {e}"
        health["status"] = "unhealthy"
    
    # Check cache
    if cache.health_check():
        health["cache"] = "healthy"
    else:
        health["cache"] = "unhealthy" if settings.CACHE_ENABLED else "disabled"
        if settings.CACHE_ENABLED:
            health["status"] = "degraded"
    
    # System resources
    try:
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        
        health["system"] = {
            "memory_usage_percent": memory.percent,
            "cpu_usage_percent": cpu_percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
        
        # Mark as unhealthy if resources are critical
        if memory.percent > 90 or cpu_percent > 90:
            health["status"] = "degraded"
            
    except Exception as e:
        health["system"] = f"error: {e}"
    
    return health


def get_detailed_health() -> Dict[str, Any]:
    """Get detailed health information."""
    health = get_health_status()
    
    # Add more detailed information
    try:
        # Database details
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            db_version = result.fetchone()[0]
            health["database_version"] = db_version
            
            # Connection pool info
            pool = engine.pool
            health["database_pool"] = {
                "size": pool.size(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "checked_in": pool.checkedin()
            }
    except Exception as e:
        health["database_error"] = str(e)
    
    # Cache details
    if cache.enabled:
        health["cache_stats"] = cache.get_cache_stats() if hasattr(cache, 'get_cache_stats') else {}
    
    # Process information
    try:
        process = psutil.Process()
        health["process"] = {
            "pid": process.pid,
            "memory_info": process.memory_info()._asdict(),
            "cpu_percent": process.cpu_percent(),
            "create_time": process.create_time(),
            "num_threads": process.num_threads()
        }
    except Exception as e:
        health["process_error"] = str(e)
    
    return health

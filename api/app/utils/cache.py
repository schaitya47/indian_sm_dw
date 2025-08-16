"""
Redis cache utilities for performance optimization.
"""

import json
import redis
from typing import Any, Optional, Union
from functools import wraps
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Redis client
redis_client = None

def get_redis_client():
    """Get Redis client instance."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            # Test connection
            redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            redis_client = None
    return redis_client


class CacheManager:
    """Cache manager for handling Redis operations."""
    
    def __init__(self):
        self.client = get_redis_client()
        self.enabled = settings.CACHE_ENABLED and self.client is not None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with TTL."""
        if not self.enabled:
            return False
        
        try:
            ttl = ttl or settings.CACHE_DEFAULT_TTL
            serialized_value = json.dumps(value, default=str)
            return self.client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        if not self.enabled:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    def health_check(self) -> bool:
        """Check Redis health."""
        if not self.client:
            return False
        
        try:
            return self.client.ping()
        except:
            return False


# Global cache manager instance
cache = CacheManager()


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments."""
    key_parts = []
    for arg in args:
        key_parts.append(str(arg))
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)


def cached(ttl: int = None, key_prefix: str = "api"):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not cache.enabled:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key_str)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key_str}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_ttl = ttl or settings.CACHE_DEFAULT_TTL
            cache.set(cache_key_str, result, cache_ttl)
            logger.debug(f"Cache set for key: {cache_key_str}")
            
            return result
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str):
    """Invalidate cache entries matching pattern."""
    return cache.delete_pattern(pattern)


def get_cache_stats() -> dict:
    """Get cache statistics."""
    if not cache.enabled:
        return {"enabled": False}
    
    try:
        info = cache.client.info()
        return {
            "enabled": True,
            "connected_clients": info.get("connected_clients", 0),
            "used_memory": info.get("used_memory_human", "0"),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "hit_rate": (info.get("keyspace_hits", 0) / 
                        max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1) * 100)
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {"enabled": False, "error": str(e)}

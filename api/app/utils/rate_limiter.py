"""
Rate limiting utilities for API throttling.
"""

import time
from typing import Dict, Optional
from collections import defaultdict, deque
from fastapi import HTTPException, Request
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter using sliding window algorithm."""
    
    def __init__(self):
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.enabled = settings.RATE_LIMIT_ENABLED
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW
    
    def is_allowed(self, key: str) -> tuple[bool, Dict[str, int]]:
        """Check if request is allowed and return rate limit info."""
        if not self.enabled:
            return True, {}
        
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        while self.requests[key] and self.requests[key][0] < window_start:
            self.requests[key].popleft()
        
        # Check if under limit
        current_requests = len(self.requests[key])
        allowed = current_requests < self.max_requests
        
        if allowed:
            self.requests[key].append(now)
        
        # Rate limit headers
        headers = {
            "X-RateLimit-Limit": self.max_requests,
            "X-RateLimit-Remaining": max(0, self.max_requests - current_requests - (1 if allowed else 0)),
            "X-RateLimit-Reset": int(now + self.window_seconds),
            "X-RateLimit-Window": self.window_seconds
        }
        
        return allowed, headers
    
    def get_key(self, request: Request) -> str:
        """Generate rate limit key from request."""
        # Use IP address as default key
        client_ip = request.client.host if request.client else "unknown"
        
        # You can extend this to use user ID, API key, etc.
        # if hasattr(request.state, "user_id"):
        #     return f"user:{request.state.user_id}"
        
        return f"ip:{client_ip}"


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(request: Request) -> Dict[str, int]:
    """Check rate limit for request and raise exception if exceeded."""
    key = rate_limiter.get_key(request)
    allowed, headers = rate_limiter.is_allowed(key)
    
    if not allowed:
        logger.warning(f"Rate limit exceeded for key: {key}")
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Too many requests.",
            headers=headers
        )
    
    return headers

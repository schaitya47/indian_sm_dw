"""
API v1 router configuration.
"""

from fastapi import APIRouter
from app.api.v1 import stocks, ohlcv, health

# Create main v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router)
api_router.include_router(stocks.router)
api_router.include_router(ohlcv.router)

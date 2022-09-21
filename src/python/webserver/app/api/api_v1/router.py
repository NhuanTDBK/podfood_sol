from fastapi import APIRouter

from app.api.api_v1.endpoints import health, inference

api_router = APIRouter()
api_router.include_router(inference.router, prefix="/ml", tags=["ml"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

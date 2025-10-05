"""
Health check endpoints for monitoring application status.
"""

from fastapi import APIRouter, Depends
import redis
import time
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "ai-audio-listener"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including dependencies."""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "ai-audio-listener",
        "checks": {}
    }

    # Check Redis connection
    try:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password
        )
        redis_client.ping()
        health_status["checks"]["redis"] = {
            "status": "healthy",
            "response_time": "OK"
        }
    except Exception as e:
        health_status["checks"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"

    # Check OpenAI API key if configured
    if settings.openai_api_key:
        health_status["checks"]["openai_api"] = {
            "status": "configured",
            "key_present": bool(settings.openai_api_key)
        }
    else:
        health_status["checks"]["openai_api"] = {
            "status": "not_configured",
            "message": "OpenAI API key not set"
        }

    return health_status


@router.get("/health/ready")
async def readiness_check():
    """Kubernetes readiness probe."""
    # Add any readiness checks here (database connections, etc.)
    return {"status": "ready"}


@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe."""
    # Simple liveness check - if the app is running, it's alive
    return {"status": "alive"}

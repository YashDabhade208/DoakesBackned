"""
FastAPI application for AI Audio Listener.
Main entry point for the application.
"""

from fastapi import FastAPI
from app.api.websocket import router as websocket_router
from app.api.audio import router as audio_router
from app.api.health import router as health_router

app = FastAPI(title="AI Audio Listener", version="1.0.0")

# Include routers
app.include_router(websocket_router)
app.include_router(audio_router)
app.include_router(health_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Audio Listener API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

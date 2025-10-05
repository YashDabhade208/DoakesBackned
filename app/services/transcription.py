"""
Transcription service for converting audio to text.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import uuid

from app.core.stt_engine import STTEngine
from app.core.redis_client import RedisClient
from app.models.audio import TranscriptionResult

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for handling audio transcription."""

    def __init__(self):
        self.stt_engine = STTEngine()
        self.redis_client = RedisClient()
        self.processing_jobs: Dict[str, Dict] = {}

    async def transcribe_audio_data(self, audio_data: bytes, job_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio data.

        Args:
            audio_data: Raw audio bytes
            job_id: Optional job identifier

        Returns:
            Transcription results
        """
        if not job_id:
            job_id = str(uuid.uuid4())

        # Store job status
        self.processing_jobs[job_id] = {
            "status": "processing",
            "start_time": asyncio.get_event_loop().time()
        }

        try:
            # Check if STT engine is available
            if not self.stt_engine.is_available():
                return {
                    "success": False,
                    "error": "Speech-to-text engine not available",
                    "job_id": job_id
                }

            # Perform transcription
            result = await self.stt_engine.transcribe_audio(audio_data)

            # Update job status
            self.processing_jobs[job_id].update({
                "status": "completed" if result["success"] else "failed",
                "end_time": asyncio.get_event_loop().time(),
                "result": result
            })

            # Cache result in Redis
            if self.redis_client.is_connected:
                cache_key = f"transcription:{job_id}"
                self.redis_client.set_json(cache_key, result, expire=3600)  # Cache for 1 hour

            return {
                "success": result["success"],
                "text": result.get("text", ""),
                "confidence": result.get("confidence", 0),
                "language": result.get("language", "unknown"),
                "job_id": job_id,
                "error": result.get("error")
            }

        except Exception as e:
            logger.error(f"Error in transcription service: {str(e)}")
            self.processing_jobs[job_id].update({
                "status": "failed",
                "end_time": asyncio.get_event_loop().time(),
                "error": str(e)
            })

            return {
                "success": False,
                "error": str(e),
                "job_id": job_id
            }

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a transcription job."""
        # Check in-memory jobs first
        if job_id in self.processing_jobs:
            return self.processing_jobs[job_id]

        # Check Redis cache
        if self.redis_client.is_connected:
            cache_key = f"transcription:{job_id}"
            cached_result = self.redis_client.get_json(cache_key)
            if cached_result:
                return {
                    "status": "completed",
                    "result": cached_result,
                    "cached": True
                }

        return None

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a transcription job."""
        if job_id in self.processing_jobs:
            self.processing_jobs[job_id].update({
                "status": "cancelled",
                "end_time": asyncio.get_event_loop().time()
            })
            return True
        return False

    def get_active_jobs(self) -> Dict[str, Dict]:
        """Get all active transcription jobs."""
        return {
            job_id: job_info
            for job_id, job_info in self.processing_jobs.items()
            if job_info.get("status") in ["processing", "pending"]
        }

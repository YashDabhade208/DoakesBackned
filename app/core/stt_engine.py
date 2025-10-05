"""
Speech-to-text engine using OpenAI Whisper.
"""

import asyncio
import logging
import os
import tempfile
from typing import Optional, Dict, Any
import openai

logger = logging.getLogger(__name__)


class STTEngine:
    """Speech-to-text engine for converting audio to text."""

    def __init__(self, api_key: Optional[str] = None, model: str = "whisper-1"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            logger.warning("OpenAI API key not provided. STT functionality will be disabled.")

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio data to text.

        Args:
            audio_data: WAV audio data as bytes

        Returns:
            Dictionary containing transcription results
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "text": ""
            }

        try:
            # Create a temporary file for the audio data
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name

            # Transcribe using OpenAI Whisper
            with open(temp_file_path, "rb") as audio_file:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file,
                        response_format="json"
                    )
                )

            # Clean up temporary file
            os.unlink(temp_file_path)

            return {
                "success": True,
                "text": response.text,
                "language": getattr(response, 'language', 'unknown'),
                "duration": getattr(response, 'duration', 0),
                "segments": getattr(response, 'segments', [])
            }

        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }

    async def transcribe_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        Transcribe an audio file from disk.

        Args:
            file_path: Path to audio file

        Returns:
            Dictionary containing transcription results
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "text": ""
            }

        try:
            with open(file_path, "rb") as audio_file:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file,
                        response_format="json"
                    )
                )

            return {
                "success": True,
                "text": response.text,
                "language": getattr(response, 'language', 'unknown'),
                "duration": getattr(response, 'duration', 0),
                "segments": getattr(response, 'segments', [])
            }

        except Exception as e:
            logger.error(f"Error transcribing audio file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }

    def is_available(self) -> bool:
        """Check if the STT engine is available for use."""
        return self.client is not None

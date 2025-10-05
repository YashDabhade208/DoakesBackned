"""
Audio data models for the AI Audio Listener application.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class AudioChunk(BaseModel):
    """Model for audio chunk data."""
    data: bytes = Field(..., description="Raw audio data")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sequence_id: int = Field(..., description="Sequence number of the chunk")
    sample_rate: int = Field(16000, description="Sample rate of audio")
    channels: int = Field(1, description="Number of audio channels")
    format: str = Field("wav", description="Audio format")


class AudioFile(BaseModel):
    """Model for uploaded audio files."""
    filename: str = Field(..., description="Original filename")
    file_id: str = Field(..., description="Unique file identifier")
    size: int = Field(..., description="File size in bytes")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    format: str = Field(..., description="Audio format")
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field("uploaded", description="Processing status")


class TranscriptionResult(BaseModel):
    """Model for transcription results."""
    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(..., description="Confidence score")
    language: str = Field("en", description="Detected language")
    duration: float = Field(..., description="Audio duration")
    segments: List[Dict[str, Any]] = Field(default_factory=list, description="Transcription segments")


class AudioProcessingRequest(BaseModel):
    """Model for audio processing requests."""
    audio_url: Optional[str] = Field(None, description="URL to audio file")
    file_id: Optional[str] = Field(None, description="ID of uploaded file")
    options: Dict[str, Any] = Field(default_factory=dict, description="Processing options")


class AudioProcessingResponse(BaseModel):
    """Model for audio processing responses."""
    success: bool = Field(..., description="Processing success status")
    result: Optional[Dict[str, Any]] = Field(None, description="Processing results")
    error: Optional[str] = Field(None, description="Error message if failed")
    processing_time: float = Field(..., description="Processing time in seconds")

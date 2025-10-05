"""
WebSocket message models for real-time communication.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Types of WebSocket messages."""
    AUDIO_CHUNK = "audio_chunk"
    TRANSCRIPTION_RESULT = "transcription_result"
    ERROR = "error"
    STATUS_UPDATE = "status_update"
    CLIENT_CONNECTED = "client_connected"
    CLIENT_DISCONNECTED = "client_disconnected"
    HEARTBEAT = "heartbeat"


class WebSocketMessage(BaseModel):
    """Base WebSocket message model."""
    type: MessageType = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    client_id: Optional[str] = Field(None, description="Client identifier")
    data: Dict[str, Any] = Field(default_factory=dict, description="Message payload")


class AudioChunkMessage(WebSocketMessage):
    """Message for audio chunk data."""
    type: MessageType = Field(MessageType.AUDIO_CHUNK, const=True)
    data: Dict[str, Any] = Field(..., description="Audio chunk data")


class TranscriptionResultMessage(WebSocketMessage):
    """Message for transcription results."""
    type: MessageType = Field(MessageType.TRANSCRIPTION_RESULT, const=True)
    data: Dict[str, Any] = Field(..., description="Transcription results")


class ErrorMessage(WebSocketMessage):
    """Message for error notifications."""
    type: MessageType = Field(MessageType.ERROR, const=True)
    data: Dict[str, Any] = Field(..., description="Error information")


class StatusUpdateMessage(WebSocketMessage):
    """Message for status updates."""
    type: MessageType = Field(MessageType.STATUS_UPDATE, const=True)
    data: Dict[str, Any] = Field(..., description="Status information")


class HeartbeatMessage(WebSocketMessage):
    """Message for heartbeat/ping."""
    type: MessageType = Field(MessageType.HEARTBEAT, const=True)
    data: Dict[str, Any] = Field(default_factory=lambda: {"ping": True})


class ClientConnectionMessage(WebSocketMessage):
    """Message for client connection events."""
    type: MessageType = Field(MessageType.CLIENT_CONNECTED, const=True)
    data: Dict[str, Any] = Field(..., description="Connection information")


class ClientDisconnectionMessage(WebSocketMessage):
    """Message for client disconnection events."""
    type: MessageType = Field(MessageType.CLIENT_DISCONNECTED, const=True)
    data: Dict[str, Any] = Field(..., description="Disconnection information")

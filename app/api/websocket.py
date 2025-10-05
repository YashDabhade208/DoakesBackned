"""
WebSocket endpoints for real-time audio streaming.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import WebSocketManager
from app.services.transcription import TranscriptionService
import json
import logging

router = APIRouter()
websocket_manager = WebSocketManager()
transcription_service = TranscriptionService()

logger = logging.getLogger(__name__)


@router.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    """WebSocket endpoint for audio streaming."""
    await websocket_manager.connect(websocket)
    client_id = id(websocket)

    try:
        while True:
            # Receive audio data from client
            data = await websocket.receive_bytes()

            # Process audio data (this would integrate with your audio processing pipeline)
            # For now, we'll just echo back that we received it
            response = {
                "type": "audio_received",
                "client_id": client_id,
                "data_size": len(data),
                "status": "processing"
            }

            await websocket_manager.send_message(client_id, json.dumps(response))

            # Here you would:
            # 1. Process the audio chunk
            # 2. Run speech-to-text if needed
            # 3. Send results back to client

    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection {client_id}: {str(e)}")
        websocket_manager.disconnect(client_id)

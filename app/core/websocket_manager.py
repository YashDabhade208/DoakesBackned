"""
WebSocket connection management for real-time communication.
"""

import json
from typing import Dict, List
import asyncio
import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time audio streaming."""

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.client_data: Dict[int, Dict] = {}

    async def connect(self, websocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        client_id = id(websocket)
        self.active_connections[client_id] = websocket
        self.client_data[client_id] = {
            "connected_at": asyncio.get_event_loop().time(),
            "status": "connected"
        }
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: int):
        """Disconnect a WebSocket client."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.client_data:
            del self.client_data[client_id]
        logger.info(f"Client {client_id} disconnected")

    async def send_message(self, client_id: int, message: str):
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to client {client_id}: {str(e)}")
                self.disconnect(client_id)

    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients."""
        disconnected_clients = []
        for client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {str(e)}")
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)

    def get_connection_count(self) -> int:
        """Get the number of active connections."""
        return len(self.active_connections)

    def get_client_info(self, client_id: int) -> Dict:
        """Get information about a specific client."""
        return self.client_data.get(client_id, {})

from fastapi import WebSocket
from typing import Dict, List
import json
import logging

logger = logging.getLogger("cara.websocket")

class ConnectionManager:
    def __init__(self):
        # Maps user_id -> List of active WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total sessions: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        """Send live adherence updates or DOSI mascot state changes to a specific user"""
        if user_id in self.active_connections:
            payload = json.dumps(message)
            for connection in self.active_connections[user_id]:
                await connection.send_text(payload)

    async def broadcast(self, message: dict):
        """Global broadcasts (e.g. maintenance warnings)"""
        payload = json.dumps(message)
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_text(payload)

manager = ConnectionManager()

from typing import List
from fastapi import WebSocket

# TODO: Check if the websocket connection is working as supposed to be or not

class ConnectionManager:
    """Manages active WebSocket client connections for real-time event broadcasting."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 [WEBSOCKET] Client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"📡 [WEBSOCKET] Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast_json(self, data: dict):
        """Broadcasts JSON payload to all connected frontend clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"⚠️ [WEBSOCKET] Error broadcasting to client: {e}")

ws_manager = ConnectionManager()
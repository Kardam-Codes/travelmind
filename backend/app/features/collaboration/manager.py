from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, trip_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[trip_id].append(websocket)

    def disconnect(self, trip_id: int, websocket: WebSocket):
        if websocket in self.active_connections[trip_id]:
            self.active_connections[trip_id].remove(websocket)

    async def broadcast(self, trip_id: int, message: dict):
        for connection in self.active_connections[trip_id]:
            await connection.send_json(message)


manager = ConnectionManager()

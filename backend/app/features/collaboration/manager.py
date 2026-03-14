from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)
        self.active_users = defaultdict(set)

    async def connect(self, trip_id: int, websocket: WebSocket, user_id: str | None = None):
        await websocket.accept()
        self.active_connections[trip_id].append(websocket)
        if user_id:
            self.active_users[trip_id].add(user_id)

    def disconnect(self, trip_id: int, websocket: WebSocket, user_id: str | None = None):
        if websocket in self.active_connections[trip_id]:
            self.active_connections[trip_id].remove(websocket)
        if user_id and user_id in self.active_users[trip_id]:
            self.active_users[trip_id].remove(user_id)

    async def broadcast(self, trip_id: int, message: dict):
        for connection in self.active_connections[trip_id]:
            await connection.send_json(message)

    def list_users(self, trip_id: int) -> list[str]:
        return sorted(self.active_users[trip_id])


manager = ConnectionManager()

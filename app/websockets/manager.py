from typing import Dict, List

from fastapi import WebSocket


# A websocket represents a single user
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket):

        # If room doesn't exist
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []

        # Add the user to the room, and prevents duplicates
        if websocket not in self.active_connections[room_id]:
            self.active_connections[room_id].append(websocket)

    # If client disconnects, remove from the specific room
    def disconnect(self, room_id: int, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        # Cleaning Empty Rooms
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    # Send the same message to all users in that room
    async def broadcast(self, room_id: int, message: dict):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_json(message)


manager = ConnectionManager()

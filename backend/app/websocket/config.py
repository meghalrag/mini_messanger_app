import json
from loguru import logger
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosedOK
from websocket import WebSocket, enableTrace

socket_response = {"success": True, "code": 200, "message": "", "data": [], "error": ""}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connection_dict: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def connect_to_group(self, websocket: WebSocket, key: str):
        await websocket.accept()
        if key not in self.connection_dict:
            self.connection_dict[key] = [websocket]
        else:
            self.connection_dict[key].append(websocket)

    def disconnect_from_group(self, websocket: WebSocket, key: str):
        self.connection_dict[key].remove(websocket)

    async def broadcast_to_group(self, key: str, message: str):
        active_conn = self.connection_dict[key]
        for connection in active_conn:
            try:
                await connection.send_text(message)
            except ConnectionClosedOK:
                pass
            except Exception as err:
                logger.error(err)


def init_connection():
    return ConnectionManager()


# def trigger_socket():
#     try:
#         data = "websocket endpoint triggered to update the posts for all users"
#         enableTrace(True)
#         ws = WebSocket()
#         ws.connect(
#             f"ws://localhost:8082/ws"
#         )
#         ws.send(data)
#         ws.close()
#     except Exception as err:
#         logger.error(f"socket trigger failed {err}")

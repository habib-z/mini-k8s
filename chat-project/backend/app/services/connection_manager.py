from fastapi import WebSocket

from app.entity.message import Message

import asyncio

class ConnectionManager:
    active_connections: dict[str, WebSocket] = {}

    @classmethod
    def connect(self, user_name: str, websocket: WebSocket):
        print(f'user_name ws: {user_name}')
        self.active_connections[user_name] = websocket

    @classmethod
    def disconnect(self, user_name: str):
        del self.active_connections[user_name]

    @classmethod
    async def send_personal_message(self, message: str, user_name: str):
        print(f'sending msg: {message} to {user_name}')
        task=asyncio.create_task(self.active_connections[user_name].send_text(message))
        await task

    @classmethod
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    @classmethod
    async def sendMessage(cls, message: Message):
        for user in message.receiver.users:
            # if user.user_name != message.sender.user_name:
                print(f'search for {user.user_name}')
                if user.user_name in cls.active_connections.keys():
                    print(f'found user for sending msg -> {user.user_name}')
                    await cls.send_personal_message(message.id, user.user_name)
                    # cls.active_connections[user.user_name].send_text(message.get_ws_string())

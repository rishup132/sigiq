import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.message_count = 0
        await self.accept()

    async def receive(self, text_data):
        self.message_count += 1
        await self.send(text_data=json.dumps({
            "count": self.message_count
        }))

    async def disconnect(self, close_code):
        print(f"[disconnect] Disconnected with total = {self.message_count}")
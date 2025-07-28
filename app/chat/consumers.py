import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.message_count = 0
        await self.channel_layer.group_add("heartbeat", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        self.message_count += 1
        await self.send(text_data=json.dumps({
            "count": self.message_count
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("heartbeat", self.channel_name)
        print(f"[disconnect] Disconnected with total = {self.message_count}")

    async def send_heartbeat(self, event):
        # Triggered by broadcast
        await self.send(text_data=json.dumps({
            "ts": event["ts"]
        }))
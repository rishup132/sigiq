import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    active_connections = set()

    async def connect(self):
        self.message_count = 0
        self.connection_id = self.channel_name
        ChatConsumer.active_connections.add(self.connection_id)
        await self.channel_layer.group_add("heartbeat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        ChatConsumer.active_connections.discard(self.connection_id)
        await self.channel_layer.group_discard("heartbeat", self.channel_name)
        print(f"[disconnect] {self.channel_name} closed with {self.message_count} messages")

    async def receive(self, text_data):
        self.message_count += 1
        await self.send(text_data=json.dumps({
            "count": self.message_count
        }))

    async def send_heartbeat(self, event):
        await self.send(text_data=json.dumps({
            "ts": event["ts"]
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.metrics import messages_total, active_connections, errors_total

class ChatConsumer(AsyncWebsocketConsumer):
    active_connections = set()

    async def connect(self):
        self.message_count = 0
        self.connection_id = self.channel_name
        ChatConsumer.active_connections.add(self.connection_id)
        await self.channel_layer.group_add("heartbeat", self.channel_name)
        await self.accept()
        active_connections.inc()

    async def disconnect(self, close_code):
        ChatConsumer.active_connections.discard(self.connection_id)
        await self.channel_layer.group_discard("heartbeat", self.channel_name)
        active_connections.dec()
        if close_code != 1001:
            print(f"[ALERT] Unexpected disconnect: {self.channel_name} code={close_code}")

        print(f"[disconnect] {self.channel_name} closed with {self.message_count} messages")

    async def receive(self, text_data):
        messages_total.inc()
        self.message_count += 1
        await self.send(text_data=json.dumps({
            "count": self.message_count
        }))

    async def send_heartbeat(self, event):
        await self.send(text_data=json.dumps({
            "ts": event["ts"]
        }))
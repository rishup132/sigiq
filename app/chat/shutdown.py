import asyncio
from channels.layers import get_channel_layer
from chat.consumers import ChatConsumer

async def graceful_shutdown():
    print("[shutdown] Graceful shutdown started")

    channel_layer = get_channel_layer()
    close_tasks = []

    for channel_name in list(ChatConsumer.active_connections):
        print(f"[shutdown] Closing {channel_name}")
        close_tasks.append(channel_layer.send(channel_name, {
            "type": "websocket.close",
            "code": 1001
        }))
        ChatConsumer.active_connections.discard(channel_name)

    if close_tasks:
        await asyncio.gather(*close_tasks)
        await asyncio.sleep(1)

    print("[shutdown] All connections closed")
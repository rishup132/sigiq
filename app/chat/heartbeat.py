import asyncio
import datetime
from channels.layers import get_channel_layer

async def heartbeat_task():
    channel_layer = get_channel_layer()
    try:
        while True:
            now = datetime.datetime.utcnow().isoformat()
            print(f"[heartbeat] Broadcasting ts = {now}")
            await channel_layer.group_send("heartbeat", {
                "type": "send.heartbeat",
                "ts": now
            })
            await asyncio.sleep(30)
    except Exception as e:
        print(f"[ALERT] Heartbeat failure: {str(e)}")
        raise
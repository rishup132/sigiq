import asyncio
import json
import pytest
import websockets

pytestmark = pytest.mark.asyncio

BASE_WS_URL = "ws://localhost:8000/ws/chat/"

async def wait_for_heartbeat(ws, timeout=5):
    try:
        message = await asyncio.wait_for(ws.recv(), timeout=timeout)
        data = json.loads(message)
        return "ts" in data
    except Exception:
        return False

async def send_and_receive(ws, msg):
    await ws.send(msg)
    response = await ws.recv()
    return json.loads(response)

@pytest.mark.asyncio
async def test_websocket_basic():
    async with websockets.connect(BASE_WS_URL) as ws:
        payload = await send_and_receive(ws, "hello")
        assert "count" in payload
        assert payload["count"] == 1

        payload = await send_and_receive(ws, "hi")
        assert "count" in payload
        assert payload["count"] == 2

        assert await wait_for_heartbeat(ws, timeout=40)

@pytest.mark.asyncio
async def test_multiple_connections():
    async with websockets.connect(BASE_WS_URL) as ws1, websockets.connect(BASE_WS_URL) as ws2:
        payload1 = await send_and_receive(ws1, "msg1")
        payload2 = await send_and_receive(ws2, "msg2")

        assert payload1["count"] == 1
        assert payload2["count"] == 1

        assert await wait_for_heartbeat(ws1, timeout=40)
        assert await wait_for_heartbeat(ws2, timeout=40)
import pytest
import asyncio
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.consumers import ChatConsumer
from channels.testing import WebsocketCommunicator

pytestmark = pytest.mark.asyncio

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns)
})

@pytest.mark.asyncio
async def test_websocket_basic():
    communicator = WebsocketCommunicator(application, "/ws/chat/")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert "count" in response

    await communicator.disconnect()
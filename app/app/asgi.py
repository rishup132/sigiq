import os
import asyncio
import datetime
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack
from chat.routing import websocket_urlpatterns
from chat.heartbeat import heartbeat_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django_asgi_app = get_asgi_application()

channels_application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": SessionMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

print("[BOOT] asgi.py loaded")

# This is the top-level ASGI app that includes lifespan + inner app
class LifespanASGIWrapper:
    def __init__(self, app):
        print("[BOOT] LifespanASGIWrapper created")
        self.app = app
        self._heartbeat_task = None

    async def __call__(self, scope, receive, send):
        print(f"[DEBUG] Scope received: {scope['type']}")
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    print("[lifespan] Startup triggered")
                    self._heartbeat_task = asyncio.create_task(heartbeat_task())
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    print("[lifespan] Shutdown triggered")
                    if self._heartbeat_task:
                        self._heartbeat_task.cancel()
                        try:
                            await self._heartbeat_task
                        except asyncio.CancelledError:
                            pass
                    await send({"type": "lifespan.shutdown.complete"})
                    break
        else:
            await self.app(scope, receive, send)

application = LifespanASGIWrapper(channels_application)
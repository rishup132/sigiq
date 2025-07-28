# load_test_ws.py
import asyncio
import websockets
import time
import json

URL = "ws://localhost:8000/ws/chat/"
CONNECTIONS = 5000
DURATION = 40  # seconds

async def wait_for_heartbeat(ws, timeout=40):
    try:
        message = await asyncio.wait_for(ws.recv(), timeout=timeout)
        data = json.loads(message)
        return "ts" in data
    except Exception:
        return False

async def worker(id, results):
    try:
        async with websockets.connect(URL) as ws:
            await ws.send("ping")
            response = await ws.recv()
            if response == '{"count": 1}' and await wait_for_heartbeat(ws):
                results["success"] += 1
    except Exception as e:
        results["failed"] += 1

async def main():
    results = {"success": 0, "failed": 0}
    tasks = [worker(i, results) for i in range(CONNECTIONS)]
    await asyncio.gather(*tasks)
    print(f"Success: {results['success']}")
    print(f"Failed: {results['failed']}")

if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    print(f"Completed in {time.time() - t0:.2f} seconds")
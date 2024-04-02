
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
import json

async def send_gesture(websocket, gesture: dict):
    try:
        # print("Sending gesture...")
        await websocket.send(json.dumps(gesture))
        # print("Gesture sent.")
    except ConnectionClosedError:
        print("WebSocket connection was closed unexpectedly.")

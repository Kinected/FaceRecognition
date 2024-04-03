
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
import json

async def send_gesture(websocket, id : str):
    try:
        # print("Sending gesture...")
        payload = {
            "userID": id
        }
        await websocket.send(json.dumps(payload))
        # print("Gesture sent.")
    except ConnectionClosedError:
        print("WebSocket connection was closed unexpectedly.")


async def send(websocket, face_names, old_face_names):
    if len(face_names) > 0:
        if len(old_face_names) == 0:
            await send_gesture(websocket, face_names[0])
              
        else : 
            if old_face_names[0] != face_names[0] or len(old_face_names) == 0:
                await send_gesture(websocket, face_names[0])
              


import cv2
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from utils.websocket.send import send, send_gesture
from utils.face_recognition.detect_faces import detect_faces
from utils.display.display_faces import display_image
from utils.requests.get_user_faces import setup_face_names_encodings
import time
import json

# Websocket URI
uri = "ws://localhost:8000/ws/faces"
uri_receive = "ws://localhost:8000/ws/new_user"


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
known_face_encodings, known_face_names = setup_face_names_encodings()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
old_face_names = []
last_face_names_sent = ""

unknown_start_time = None

async def receive_messages(websocket):
    print(websocket)
    async for message in websocket:
        json_message = json.loads(message)
        known_face_encodings.append(json_message["face"])
        known_face_names.append(str(json_message["userID"]))
        print(f"Received message !")


async def process_images(websocket):
    global process_this_frame
    global old_face_names
    global unknown_start_time
    while True:   
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            face_names, face_locations = await detect_faces(frame, known_face_encodings, known_face_names)

            if len(face_names) > 0:
                if face_names[0] == "Unknown":
                    if unknown_start_time is None:
                        unknown_start_time = time.time() 
                    elif time.time() - unknown_start_time >= 2:  

                        await send_gesture(websocket, "Unknown")
                        unknown_start_time = None
                else:
                    unknown_start_time = None  
                    await send(websocket, face_names, old_face_names)
            
        process_this_frame = not process_this_frame
        old_face_names = face_names

        # Display the frame
        display_image(frame, face_locations, face_names)

        await asyncio.sleep(0)


async def main():
    global unknown_start_time
    while True:
        try:
            print("Connecting to server...")
            async with websockets.connect(uri) as websocket:
                async with websockets.connect(uri_receive) as websocket_receive:
                    print("Connected to server.")
                    receive_task = asyncio.create_task(receive_messages(websocket_receive))
                    process_images_task = asyncio.create_task(process_images(websocket))
                    await asyncio.gather(receive_task, process_images_task)

        except ConnectionClosed:
            print("Connection lost. Reconnecting...")
            continue
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"Server rejected WebSocket connection: {e}")
            break

asyncio.run(main())

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
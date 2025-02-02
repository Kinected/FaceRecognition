import asyncio
import cv2
import json
import time
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError

from utils.display.display_faces import display_image
from utils.face_recognition.detect_faces import detect_faces
from utils.face_recognition.resize import frame_preprocessing
from utils.requests.get_user_faces import setup_face_names_encodings
from utils.websocket.connect import create_connection
from utils.websocket.send import send, send_gesture

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
new_face_start_time = None


async def receive_messages(websocket):
    while True:
        try:
            print(websocket)
            async for message in websocket:
                print(f"Received message !")
                json_message = json.loads(message)
                if json_message["type"] == True:
                    known_face_encodings.append(json_message["face"])
                    known_face_names.append(str(json_message["userID"]))
                else:
                    known_face_encodings.pop(known_face_names.index(str(json_message["userID"])))
                    known_face_names.remove(str(json_message["userID"]))

            break  # Si la réception est réussie, on sort de la boucle
        except ConnectionClosedError:
            print("WebSocket connection was closed unexpectedly.")
            print("Reconnecting...")
            websocket = await create_connection(uri_receive)


async def process_images(websocket):
    global process_this_frame
    global old_face_names
    global unknown_start_time
    global new_face_start_time
    global last_face_names_sent
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = frame_preprocessing(frame, resize_to=(640, 640))

        # Only process every other frame of video to save time
        if process_this_frame:
            face_names, face_locations = await detect_faces(frame, known_face_encodings, known_face_names)

            if len(face_names) > 0:

                if len(old_face_names)>0:
                    if face_names[0] != old_face_names[0]:
                        unknown_start_time = None

                if unknown_start_time is None:
                    unknown_start_time = time.time()
                elif time.time() - unknown_start_time >= 2:
                    print("Sending gesture...")
                    status = await send_gesture(websocket, face_names[0])
                    if not status:
                        print("Reconnecting...")
                        websocket = await create_connection(uri)
                    unknown_start_time = None
            old_face_names = face_names

        process_this_frame = not process_this_frame

        # Display the frame
        if len(face_locations) > 0:
            display_image(frame, [face_locations[0]], [face_names[0]])
        else:
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

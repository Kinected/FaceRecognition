import cv2
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from utils.websocket.send import send_gesture
from utils.face_recognition.detect_faces import detect_faces
from utils.display.display_faces import display_image
from utils.requests.get_user_faces import setup_face_names_encodings

# Websocket URI
uri = "ws://localhost:8000/ws/faces"

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
known_face_encodings, known_face_names = setup_face_names_encodings()
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

async def main():
    global process_this_frame
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    # Grab a single frame of video
                    ret, frame = video_capture.read()

                    # Only process every other frame of video to save time
                    if process_this_frame:
                        face_names, face_locations = await detect_faces(frame, known_face_encodings, known_face_names)

                        if len(face_names) > 0:
                            payload = {
                                "userID": face_names[0]
                            }
                            await send_gesture(websocket, payload)

                    process_this_frame = not process_this_frame


                    #Display the frame
                    display_image(frame, face_locations, face_names)

                    

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

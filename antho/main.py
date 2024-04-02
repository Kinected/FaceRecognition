import face_recognition
import cv2
import numpy as np
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
import json

uri = "ws://localhost:8000/ws/swipes"

font = cv2.FONT_HERSHEY_DUPLEX




async def send_gesture(websocket, gesture: dict):
    try:
        # print("Sending gesture...")
        await websocket.send(json.dumps(gesture))
        # print("Gesture sent.")
    except ConnectionClosedError:
        print("WebSocket connection was closed unexpectedly.")


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a third sample picture and learn how to recognize it.
antoine_image = face_recognition.load_image_file("antoine.jpg")
antoine_face_encoding = face_recognition.face_encodings(antoine_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    antoine_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Antoine Maes"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

async def detect_faces(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

                        
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    return face_names, face_locations   



def display_image(frame, face_locations, face_names):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    cv2.waitKey(1)
    


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
                        face_names, face_locations = await detect_faces(frame)

                        if len(face_names) > 0:
                            payload = {
                                "swipe": face_names[0]
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

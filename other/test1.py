
import face_recognition

marie = face_recognition.load_image_file("antoine.jpg")
marie_encoding = face_recognition.face_encodings(marie)[0]

print(marie_encoding.tolist())
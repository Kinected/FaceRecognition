# from utils.requests.get_user_faces import setup_face_names_encodings

# known_face_encodings, known_face_names = setup_face_names_encodings()

# print(known_face_encodings)
# print(known_face_names)


import face_recognition

marie = face_recognition.load_image_file("sam2.jpg")
marie_encoding = face_recognition.face_encodings(marie)[0]

print(marie_encoding.tolist())
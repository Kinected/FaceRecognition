from utils.requests.get_user_faces import setup_face_names_encodings

known_face_encodings, known_face_names = setup_face_names_encodings()

print(known_face_encodings)
print(known_face_names)

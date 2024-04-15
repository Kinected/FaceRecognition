import requests
import numpy as np



def get_user_faces():
    response = requests.get('http://localhost:8000/api/user/face/all')

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Requête échouée avec le statut: {response.status_code}')
        return None




def setup_face_names_encodings():
    # Get a list of users and their faces
    users = get_user_faces()

    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names = []

    for user in users:
        known_face_encodings.append(np.array(user['face']))
        known_face_names.append(str(user['id']))

    return known_face_encodings, known_face_names
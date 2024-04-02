import cv2 as cv
from time import perf_counter
import os

webcam = cv.VideoCapture(0)

if not webcam.isOpened():
    print("Erreur lors de l'ouverture de la webcam.")
    exit()

# Lecture d'un certain nombre d'images
NB_IMAGES = 100
frame_count = 0

while frame_count < NB_IMAGES:
    bImgReady, imageframe = webcam.read()
    if not bImgReady:
        print('Aucune image disponible.')
        break
    frame_count += 1

webcam.release()
cv.destroyAllWindows()

# Chemin vers le fichier XML
dirCascadeFiles = ''

# Nom du fichier XML
xml_filename = "haarcascade_frontalface_default.xml"

# Chemin complet vers le fichier XML
xml_path = os.path.join(dirCascadeFiles, xml_filename)

# Vérification de l'existence du fichier XML
if not os.path.exists(xml_path):
    print(f"Le fichier XML du classificateur en cascade ({xml_filename}) n'a pas été trouvé dans le dossier spécifié.")
    exit()

# Chargement du classificateur en cascade
classCascadefacial = cv.CascadeClassifier(xml_path)

def facialDetectionAndMark(_image, _classCascade):
    imgreturn = _image.copy()
    gray = cv.cvtColor(imgreturn, cv.COLOR_BGR2GRAY)
    faces = _classCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv.rectangle(imgreturn, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return imgreturn

def videoDetection(_haarclass):
    webcam = cv.VideoCapture(0)
    if not webcam.isOpened():
        print("Erreur lors de l'ouverture de la webcam.")
        exit()

    while True:
        bImgReady, imageframe = webcam.read()
        if not bImgReady:
            print('Aucune image disponible.')
            break
        face = facialDetectionAndMark(imageframe, _haarclass)
        cv.imshow('Ma webcam', face)
        keystroke = cv.waitKey(20)
        if keystroke == 27:
            break

    webcam.release()
    cv.destroyAllWindows()

videoDetection(classCascadefacial)

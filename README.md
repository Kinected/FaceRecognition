# Kinected/FaceRecognition

# Requirements

## Packages 
- websockets
- opencv-python
- face_recognition
- numpy

## Hardware
#### Une webcam (oui oui)


# Setup

## Django

### Si utilise Kinected/Back (https://github.com/Kinected/Back)
#### Lancer le serveur
```bash
python manage.py runserver 
```
#### Avoir des utilisateurs (UserProfile) crée au préalable avec un visage (Face)


### Sinon
#### Avoir un serveur websockets fonctionnel 
- Lancer le container Docker (Redis)
- Avoir des channels pour traiter les routes websocket :
  -  ws://localhost:8000/ws/faces
  -  ws://localhost:8000/ws/new_user
#### Lancer le serveur
```bash
python manage.py runserver 
```

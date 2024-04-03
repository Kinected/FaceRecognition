import asyncio
import websockets

async def receive_messages(uri):
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(f"Received message: {message}")

# Remplacez 'ws://localhost:8765' par l'URI de votre serveur WebSocket
asyncio.run(receive_messages("ws://localhost:8000/ws/new_user"))
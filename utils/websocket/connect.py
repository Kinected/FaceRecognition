import websockets
import asyncio

async def create_connection(uri):
    while True:
        try:
            print("Connecting to server...")
            websocket = await websockets.connect(uri)
            print("Connected to server.")
            return websocket
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Attendre avant de tenter de se reconnecter
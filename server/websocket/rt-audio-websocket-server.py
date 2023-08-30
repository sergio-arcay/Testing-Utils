import asyncio
import websockets
import sounddevice as sd
import numpy as np

class AudioServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def handle_client(self, websocket, path):
        print("New client connected")
        try:
            while True:
                audio_data_bytes = await websocket.recv()
                audio_data = np.frombuffer(audio_data_bytes, dtype=np.int16).astype(np.float32) / 32767.0
                sd.play(audio_data, samplerate=44100)
                # He eliminado sd.wait() para permitir una reproducción más fluida
        except Exception as e:
            print("Error while handling client:", e)
        finally:
            print("Client disconnected")

    def start(self):
        loop = asyncio.get_event_loop()
        server = websockets.serve(self.handle_client, self.host, self.port)
        loop.run_until_complete(server)
        print(f"Server started at ws://{self.host}:{self.port}")
        loop.run_forever()

if __name__ == "__main__":
    audio_server = AudioServer("0.0.0.0", 8765)
    audio_server.start()

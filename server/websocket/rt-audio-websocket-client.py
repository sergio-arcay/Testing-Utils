import asyncio
import websockets
import sounddevice as sd
import numpy as np

def calculate_rms(audio_data):
    """Calcula el nivel RMS del audio."""
    return np.sqrt(np.mean(np.square(audio_data)))

async def stream_audio_to_server():
    async with websockets.connect("ws://127.0.0.1:8765") as websocket:
        with sd.InputStream(samplerate=44100, channels=2, device=2) as stream:
            while True:
                audio_data, overflowed = stream.read(4410)

                # Calcula y muestra el nivel RMS del audio.
                rms_level = calculate_rms(audio_data)
                print(f"RMS Level: {rms_level:.5f}")

                if overflowed:
                    print("Warning: Input overflowed. Some audio data might be lost.")

                audio_bytes = (audio_data * 32767).astype(np.int16).tobytes()  # Convertir float32 a int16
                await websocket.send(audio_bytes)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(stream_audio_to_server())

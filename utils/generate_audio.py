import edge_tts
import os

AUDIO_PATH = os.path.join(os.getenv("AUDIO_DIR", "/tmp"), "speech.mp3")

async def generate_audio(text):
    communicate = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural")
    await communicate.save(AUDIO_PATH)

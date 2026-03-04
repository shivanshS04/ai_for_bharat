import edge_tts
import os

async def generate_audio(text):
    # Resolve path at call time so AUDIO_DIR env var (loaded via dotenv) is always respected
    audio_path = os.path.join(os.getenv("AUDIO_DIR", "/tmp"), "speech.mp3")
    communicate = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural")
    await communicate.save(audio_path)

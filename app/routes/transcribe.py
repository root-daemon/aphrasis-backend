from fastapi import APIRouter, File, UploadFile, HTTPException
from pydub import AudioSegment
# from huggingface_hub import InferenceClient  # Commented out Hugging Face import
import io
import os
from dotenv import load_dotenv

load_dotenv()

transcribe_router = APIRouter()
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Hugging Face client - COMMENTED OUT
# HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
# if not HF_TOKEN:
#     raise ValueError("HUGGINGFACE_TOKEN environment variable is not set")

# client = InferenceClient(token=HF_TOKEN)

@transcribe_router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        audio_file = io.BytesIO(file_bytes)
        audio = AudioSegment.from_file(audio_file)

        # Convert to WAV and save temporarily
        wav_file = io.BytesIO()
        audio.export(wav_file, format="wav")
        wav_file.seek(0)
        wav_file_location = os.path.join(UPLOAD_FOLDER, "converted_audio.wav")
        with open(wav_file_location, "wb") as f:
            f.write(wav_file.read())

        # HUGGING FACE TRANSCRIPTION COMMENTED OUT
        # # Use Hugging Face's Whisper API for transcription
        # with open(wav_file_location, "rb") as f:
        #     result = client.audio_transcription(
        #         data=f,
        #         model="openai/whisper-base"
        #     )

        # Clean up the temporary file
        os.remove(wav_file_location)

        # Return dummy response instead of actual transcription
        return {
            "message": "Transcription endpoint disabled",
            "transcription": "Hugging Face functionality has been disabled. This is a placeholder response.",
        }

    except Exception as e:
        if os.path.exists(wav_file_location):
            os.remove(wav_file_location)
        raise HTTPException(status_code=500, detail=str(e))
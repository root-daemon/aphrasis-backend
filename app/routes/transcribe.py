from fastapi import APIRouter,File,UploadFile
from pydub import AudioSegment
import io
import os

transcribe_router = APIRouter()
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

@transcribe_router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        audio_file = io.BytesIO(file_bytes)

        audio = AudioSegment.from_file(audio_file)

        wav_file = io.BytesIO()
        audio.export(wav_file, format="wav")

        wav_file.seek(0)  
        wav_file_location = os.path.join(UPLOAD_FOLDER, "converted_audio.wav")
        with open(wav_file_location, "wb") as f:
            f.write(wav_file.read())

        return {"message": "Audio converted to WAV successfully!"}

    except Exception as e:
        return {"message": f"Error: {e}"}
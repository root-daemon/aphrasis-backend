from fastapi import APIRouter,File, UploadFile
from app.utils.audio_utils import convert_wav, get_file_extension,transcribe_audio
from app.utils.file_utils import download_audio_file

transcribe_router = APIRouter()

@transcribe_router.post('/')
async def transcribe(file: UploadFile = File(...)):
    audio_data = await file.read()
    transcription = transcribe_audio(audio_data, file.filename)
    return {"transcription": transcription}

@transcribe_router.post('/url')
async def transcribe_url(url: str):
    audio_file_path = download_audio_file(url)
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    transcription = transcribe_audio(audio_data, audio_file_path)
    return {"transcription": transcription}
from fastapi import APIRouter

transcribe_router = APIRouter()

@transcribe_router.get("/transcribe")
def transcribe():
    return {"message":"Transcribe Route"}
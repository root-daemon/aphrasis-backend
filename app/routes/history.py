from fastapi import APIRouter, HTTPException
from app.database.supabase_utils import supabase

history_router = APIRouter()

@history_router.get("/history_data/{uuid}")
async def history_data(uuid: str):
    try:
        history_data = supabase.table("history").select("file_name", "transcription").eq("uuid", uuid).execute()

        if not history_data.data:
                raise HTTPException(status_code=404, detail=f"No history records found for user {uuid}")
        base_url="https://gdvvfpvgmfjrrwzzkitv.supabase.co/storage/v1/object/public/audio_files/"
        
        response_data = []
        for record in history_data.data:
            file_url = base_url + record["file_name"]
            transcription = record["transcription"]
            
            response_data.append({
                "audio_url": file_url, 
                "transcription": transcription
            })
            
        return response_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching audio data for user {uuid}: {str(e)}")
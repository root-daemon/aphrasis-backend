from fastapi import APIRouter,HTTPException
from database.supabase_utils import supabase

progress_router = APIRouter()

@progress_router.get("/level/{uuid}")
def level(uuid: str):
    try:
        response = supabase.table("user_progress").select("level_id","accuracy","attempts").eq("uuid", uuid).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Level not found")
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching level: {str(e)}")
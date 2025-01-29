from fastapi import APIRouter,HTTPException
from database.supabase_utils import supabase

level_router = APIRouter()

@level_router.get("/levels_data/{uuid}")
def level_data(uuid:str):
    try:
        level_response = supabase.table("levels").select("level_id","title","sentence").execute()
        progress_response = supabase.table("user_progress").select("level_id","accuracy","attempts").eq("uuid",uuid).execute()
        
        if not level_response.data:
            raise HTTPException(status_code=404, detail="Practice data not found")
      
        user_progress = {entry["level_id"]: {"accuracy": entry["accuracy"], "attempts": entry["attempts"]} for entry in progress_response.data}
        print(user_progress)
        levels_with_progress = [
            {
                "level_id": level["level_id"],
                'title': level["title"],
                "sentence": level["sentence"],
                "progress": user_progress[level["level_id"]]
            }
            for level in level_response.data
        ]

        return levels_with_progress
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching practice data: {str(e)}")
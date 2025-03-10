from fastapi import APIRouter,HTTPException
from database.supabase_utils import supabase
from schemas.user_schema import LevelProgressUpdateSchema

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


@level_router.put("/level_progress/{uuid}/{level_id}")
async def update_level_progress(uuid: str, level_id: int, data: LevelProgressUpdateSchema):
    try:
        # First, check if a progress record exists
        existing_progress = supabase.table("user_progress").select("*").eq("uuid", uuid).eq("level_id", level_id).execute()
        
        if existing_progress.data:
            # If record exists, update it with incremented attempts
            current_attempts = existing_progress.data[0]["attempts"]
            response = supabase.table("user_progress").update({
                "accuracy": data.accuracy,
                "attempts": current_attempts + 1
            }).eq("uuid", uuid).eq("level_id", level_id).execute()
        else:
            # If no record exists, create a new one with attempts = 1
            response = supabase.table("user_progress").insert({
                "uuid": uuid,
                "level_id": level_id,
                "accuracy": data.accuracy,
                "attempts": 1
            }).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Failed to update progress")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating level progress: {str(e)}")
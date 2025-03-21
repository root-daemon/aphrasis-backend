from fastapi import APIRouter,HTTPException
from app.database.supabase_utils import supabase
from app.schemas.user_schema import LevelProgressUpdateSchema
from typing import Optional

level_router = APIRouter()

@level_router.get("/levels_data/{uuid}")
def level_data(uuid:str):
    try:
        level_response = supabase.table("levels").select("level_id","title","sentence").order("level_id").execute()
        if not level_response.data:
            raise HTTPException(status_code=404, detail="Practice data not found")

        progress_response = supabase.table("user_progress").select("level_id","accuracy","attempts").eq("uuid",uuid).execute()
        
        user_progress = {}
        for level in level_response.data:
            user_progress[level["level_id"]] = {"accuracy": 0, "attempts": 0}
        
        for entry in progress_response.data:
            user_progress[entry["level_id"]] = {
                "accuracy": entry["accuracy"],
                "attempts": entry["attempts"]
            }
        
        levels_with_progress = []
        previous_level_completed = True
        
        for level in level_response.data:
            current_progress = user_progress[level["level_id"]]
            is_locked = not previous_level_completed and level["level_id"] != 1
            
            previous_level_completed = current_progress["accuracy"] >= 50
            
            levels_with_progress.append({
                "level_id": level["level_id"],
                "title": level["title"],
                "sentence": level["sentence"],
                "progress": current_progress,
                "is_locked": is_locked
            })

        return levels_with_progress
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching practice data: {str(e)}")


@level_router.put("/level_progress/{uuid}/{level_id}")
async def update_level_progress(uuid: str, level_id: int, data: LevelProgressUpdateSchema):
    try:
        existing_progress = supabase.table("user_progress").select("*").eq("uuid", uuid).eq("level_id", level_id).execute()
        
        if existing_progress.data:
            current_attempts = existing_progress.data[0]["attempts"]
            response = supabase.table("user_progress").update({
                "accuracy": data.accuracy,
                "attempts": current_attempts + 1
            }).eq("uuid", uuid).eq("level_id", level_id).execute()
        else:
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

@level_router.get("/levels")
async def get_all_levels():
    try:
        response = supabase.table("levels").select("*").order("level_id").execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="No levels found")
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching levels: {str(e)}")

@level_router.get("/level/{level_id}")
async def get_level(level_id: int, uuid: Optional[str] = None):
    try:
        level_response = supabase.table("levels").select("*").eq("level_id", level_id).execute()
        
        if not level_response.data:
            raise HTTPException(status_code=404, detail=f"Level {level_id} not found")
        
        level_data = level_response.data[0]
        
        if uuid:
            progress_response = supabase.table("user_progress").select("accuracy", "attempts").eq("uuid", uuid).eq("level_id", level_id).execute()
            
            if level_id > 1:
                prev_progress = supabase.table("user_progress").select("accuracy").eq("uuid", uuid).eq("level_id", level_id - 1).execute()
                is_locked = not prev_progress.data or prev_progress.data[0]["accuracy"] < 80
            else:
                is_locked = False
            
            progress = progress_response.data[0] if progress_response.data else {"accuracy": 0, "attempts": 0}
            
            return {
                **level_data,
                "progress": progress,
                "is_locked": is_locked
            }
        
        return level_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching level data: {str(e)}")

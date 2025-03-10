from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserSchema
from app.database.supabase_utils import supabase

user_router = APIRouter()


@user_router.get("/user/{uuid}")
def user(uuid: str):
    try:
        response = supabase.table("users").select("name","streak","level_completed").eq("uuid", uuid).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


@user_router.post("/user")
def new_user(data: UserSchema):
    try:
        existing_user = supabase.table("users").select("name","streak","level_completed").eq('uuid', data.uuid).execute()
        if existing_user.data:
            return existing_user.data[0]


        user_response = supabase.table("users").insert([data.model_dump()]).execute()
        
        levels_response = supabase.table("levels").select("level_id").order("level_id").execute()
        
        if levels_response.data:
            progress_entries = [
                {
                    "uuid": data.uuid,
                    "level_id": level["level_id"],
                    "accuracy": 0,
                    "attempts": 0
                }
                for level in levels_response.data
            ]
            
            supabase.table("user_progress").insert(progress_entries).execute()
        
        return {"user": data.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
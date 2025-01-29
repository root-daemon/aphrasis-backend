from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserSchema
from database.supabase_utils import supabase

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
        existing_user = supabase.table("users").select('uuid').eq('uuid', data.uuid).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="User already exists")
        else:
            supabase.table("users").insert([data.dict()]).execute()
        return {"user": data.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
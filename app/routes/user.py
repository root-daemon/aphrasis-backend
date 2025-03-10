from fastapi import APIRouter
from schemas.user_schema import UserSchema
from database.supabase_utils import supabase

user_router = APIRouter()


@user_router.get("/user/{uuid}")
def user(uuid: str):
    try:
        response = supabase.table("users").select("name","streak","levels").eq("uuid", uuid).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


@user_router.post("/user")
def new_user(data: UserSchema):
    return {"message":"New User Route"}
from fastapi import APIRouter
from schemas.user_schema import UserSchema

user_router = APIRouter()


@user_router.get("/user/{uuid}")
def user(uuid: str):
    return {"message":"Transcribe Route"}

@user_router.post("/user")
def new_user(data: UserSchema):
    return {"message":"New User Route"}
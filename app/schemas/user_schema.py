from pydantic import BaseModel

class UserSchema(BaseModel):
    uuid: str
    name: str
    email: str
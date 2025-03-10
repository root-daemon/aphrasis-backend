from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    uuid: str
    name: str
    email: str

class LevelProgressUpdateSchema(BaseModel):
    accuracy: float
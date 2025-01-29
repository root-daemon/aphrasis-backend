from fastapi import FastAPI
from app.routes.transcribe import transcribe_router
from app.routes.user import user_router
from app.routes.levels import level_router

app = FastAPI()

app.include_router(transcribe_router,prefix="/api",tags=["Transcribe"])
app.include_router(user_router,prefix="/api",tags=["User"])
app.include_router(level_router,prefix="/api",tags=["Levels"])

@app.get("/")
def main():
    return {"message":"Server Running"}


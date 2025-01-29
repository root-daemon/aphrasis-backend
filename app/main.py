from fastapi import FastAPI
from routes.transcribe import transcribe_router
from routes.user import user_router

app = FastAPI()

app.include_router(transcribe_router,prefix="/api",tags=["Transcribe"])
app.include_router(user_router,prefix="/api",tags=["User"])

@app.get("/")
def main():
    return {"message":"Server Running"}


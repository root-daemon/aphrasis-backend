from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.transcribe import transcribe_router
from app.routes.user import user_router
from app.routes.levels import level_router
from app.routes.history import history_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://aphrasis-blush.vercel.app/", 'https://cron-job.org',
      'https://cron-job.org/cron-job-scheduler-online/'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router,prefix="/api",tags=["Transcribe"])
app.include_router(user_router,prefix="/api",tags=["User"])
app.include_router(level_router,prefix="/api",tags=["Levels"])
app.include_router(history_router,prefix="/api",tags=["History"])

@app.get("/")
def main():
    return {"message":"Server Running"}


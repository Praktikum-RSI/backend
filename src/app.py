from fastapi import FastAPI

from src.routers.event import router as event_router

app = FastAPI()

app.include_router(event_router)

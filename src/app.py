from fastapi import FastAPI

from src.routers.event import router as event_router
from src.routers.login import router as login_router
from src.routers.register import router as register_router

app = FastAPI()

app.include_router(event_router)
app.include_router(register_router)
app.include_router(login_router)

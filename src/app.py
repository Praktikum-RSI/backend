from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middlewares.auth import AuthMiddleware, ProtectedRoute
from src.middlewares.error import register_exception_handlers
from src.routers.auth import auth_router
from src.routers.event import event_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.add_middleware(
    AuthMiddleware,
    protected_routes=[
        ProtectedRoute("/logout", ["POST"], exact=True),
        ProtectedRoute("/events/", ["POST"], exact=False),
    ],
    admin_routes=[
        ProtectedRoute("/events", ["POST"], exact=True),
        ProtectedRoute("/events/", ["POST"], exact=True),
        ProtectedRoute("/events/", ["PATCH", "DELETE"], exact=False),
    ],
)


app.include_router(auth_router)
app.include_router(event_router)

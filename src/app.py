from fastapi import FastAPI

from src.middlewares.auth import AuthMiddleware, ProtectedRoute
from src.middlewares.error import register_exception_handlers
from src.routers.auth import auth_router
from src.routers.event import event_router

app = FastAPI()

register_exception_handlers(app)


app.add_middleware(
    AuthMiddleware,
    protected_routes=[
        ProtectedRoute("/logout", ["POST"]),
    ],
    admin_routes=[
        ProtectedRoute("/events", ["POST", "PATCH", "DELETE"]),
    ],
)


app.include_router(auth_router)
app.include_router(event_router)

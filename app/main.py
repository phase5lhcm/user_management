from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.models.event import Event
from contextlib import asynccontextmanager
from app.utils.security import hash_password
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
from fastapi.routing import APIRoute
import traceback

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    Database.initialize(settings.database_url, echo=settings.debug)

    async with Database._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    lifespan=lifespan 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print("Unhandled Exception:", traceback.format_exc()) 
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})
from fastapi import FastAPI

from dotenv import load_dotenv
import os
from app.api.routers.index import Tags
from app.api.routers.v1.user_router import userrouter
from app.api.routers.v1.auth_router import authrouter
from app.infrastructure.database.database_init import sessionmanager, Base

load_dotenv()  # read file .env

app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("API_VERSION"),
    openapi_tags=Tags,
)

async def startup():
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(userrouter)
app.include_router(authrouter)
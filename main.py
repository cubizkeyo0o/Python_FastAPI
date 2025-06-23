import uvicorn
from fastapi import FastAPI

from app.API.Routers.Index import Tags
from app.Infrastructure.Config.Enviroment import get_enviroment_variables
from app.API.Routers.v1.UserRouter import userrouter
from app.API.Routers.v1.AuthRouter import authrouter
from app.domain.Base import Base
from app.Infrastructure.database.DatabaseInit import sessionmanager

env = get_enviroment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

async def startup():
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(userrouter)
app.include_router(authrouter)
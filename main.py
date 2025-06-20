import uvicorn
from fastapi import FastAPI

from app.API.Routers.Index import Tags
from app.Infrastructure.Config.Enviroment import get_enviroment_variables
from app.API.Routers.v1.UserRouter import userrouter

env = get_enviroment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

app.include_router(userrouter)
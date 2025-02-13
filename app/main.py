from fastapi import FastAPI

from Infrastructure.Config import Tags
from Infrastructure.Config.Enviroment import get_environment_variables
from Domain.Entities.Base import init
from API.Routers.v1 import UserRouter

env = get_environment_variables()

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

app.include_router()

@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.post("/createuser")
def get_all_user():
    return UserRouter.get_all_user()


@app.patch("/updateuser/{userId}")
def get_user_by_id(userId: int):
    return UserRouter.get_user_by_id(userId)

init()
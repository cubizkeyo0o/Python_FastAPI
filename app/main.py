from fastapi import FastAPI

from app import api
from config.tags import Tags
from config.enviroment import get_environment_variables

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


@app.get("/createuser")
def get_all_user():
    return api.get_all_user()


@app.get("/updateuser/{userId}")
def get_user_by_id(userId: int):
    return api.get_user_by_id(userId)
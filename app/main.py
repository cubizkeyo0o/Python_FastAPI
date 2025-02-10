from fastapi import FastAPI

from app.api import api

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/getalluser")
def get_all_user():
    return api.get_all_user()


@app.get("/getuserbyid/{userId}")
def get_user_by_id(userId: int):
    return api.get_user_by_id(userId)
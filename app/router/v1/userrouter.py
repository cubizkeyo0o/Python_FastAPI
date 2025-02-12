from typing import List, Optional

from fastapi import APIRouter, Depends, status
from service import userservice

userrouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

userrouter.post(
    "/",
    response_model=AuthorSchema,
    status_code=status.HTTP_201_CREATED,
)
def create(
    author: AuthorPostRequestSchema,
    authorService: AuthorService = Depends(),
    ):
    return use.create(author).normalize()

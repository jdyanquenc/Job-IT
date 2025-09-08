from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from . import  models
from . import service
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import DbSession

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: DbSession):
    return service.login_for_access_token(form_data, db)








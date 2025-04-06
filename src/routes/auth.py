
from typing import Annotated

from fastapi import  APIRouter, Response, status, Form,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import UserModel
from ..db.index import get_db
from ..schema.auth import CreateIUserDict,GetFullUser, UserLogin
from ..services.auth import  register_crud, login_crud,check_auth_services
from ..utils.auth import UserRepositoryUtils
from ..dependencies.auth import get_user_repo, get_current_user

from rich import print


route = APIRouter(tags=["auth"])




@route.post("/signup", status_code= status.HTTP_201_CREATED)
async def signup_route(
    user_model: Annotated[CreateIUserDict, Form()],
    user_repo: Annotated[UserRepositoryUtils,  Depends(get_user_repo)],):
  result = await register_crud(user_model,user_repo)

  return result


@route.post("/login", status_code= status.HTTP_202_ACCEPTED, response_model=GetFullUser)
async def login_route(
    form_data: Annotated[UserLogin, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],response: Response):
  res = await login_crud(db,form_data,response)
  return res

@route.post("/logout", status_code= status.HTTP_204_NO_CONTENT)
async def logout_route(current_user: Annotated[UserModel, Depends(get_current_user)],response: Response):
  response.delete_cookie("access_token")

@route.get('/check-auth', response_model=GetFullUser, status_code=status.HTTP_200_OK)
async def get_user_me_router( current_user: Annotated[UserModel, Depends(check_auth_services)]):
  return current_user









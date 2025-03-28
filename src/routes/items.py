
from typing import Annotated,List

from fastapi import  APIRouter, Response, status, Form,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import UserModel,ItemsModel
from ..db.index import get_db
from ..schema.auth import CreateIUserDict,GetFullUser, UserLogin
from ..services.auth import  register_crud, login_crud,check_auth_services
from ..utils.auth import UserRepositoryUtils
from ..dependencies.auth import get_user_repo, get_current_user

from rich import print


route = APIRouter(tags=["Items"])



@route.get('/', status_code= status.HTTP_200_OK)
async def get_all_items():
  return {
    'items': 'All items'
  }







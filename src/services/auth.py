from typing import  Annotated
from datetime import datetime, timezone

from rich import print

from fastapi.encoders import jsonable_encoder
from fastapi import Response, HTTPException, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.auth import get_current_user
from ..db.models import UserModel
from ..schema.auth import CreateIUserDict, UserLogin
from ..utils.auth import (
  hash_password_utils,
  UserRepositoryUtils,
  create_token,
  validate_user_data,
  authenticate_user
)




#? user sign up function

async def register_crud(db: AsyncSession, user_model: CreateIUserDict,user_repo: UserRepositoryUtils) -> dict:

  user = await validate_user_data(db,user_model)

  hashing = hash_password_utils(user.password)
  user_data = user.model_dump()
  user_data['password'] = hashing

  user = await user_repo.create(**user_data)
  return user


#? user login function
async def login_crud(db: AsyncSession,form_data: UserLogin, response: Response):

  user_repo = UserRepositoryUtils(db)
  user = await authenticate_user(user_repo,form_data)
  
  token_dict = {
    "sub": str(user.uid),
    "email": user.email
  }
  user.last_login_date = datetime.now(timezone.utc)
  await db.commit()
  await db.refresh(user)
  
  await create_token(token_dict,response)
  return user


async def check_auth_services(current_user: Annotated[UserModel, Depends(get_current_user)] )-> UserModel:
  try:
    return  current_user
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))





















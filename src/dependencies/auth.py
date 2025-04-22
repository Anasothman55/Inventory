from ..db.models import UserModel
from ..utils.auth import UserRepositoryUtils, jwt_decode
from ..db.index import get_db
from ..exceptions.auth import UserNotFoundError, AuthorizationError
from ..schema.auth import RoleBase

from rich import print

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated, List
import uuid

async def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]):
  return UserRepositoryUtils(db)


async def get_access_token(request: Request):
  if not (access_token := request.cookies.get("access_token")):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Access Token is missing",
    )
  return access_token


async def get_current_user(
    access_token: Annotated[str, Depends(get_access_token)],
    user_repo: Annotated[UserRepositoryUtils, Depends(get_user_repo)])-> UserModel:

  payload = jwt_decode(access_token)
  user_id = uuid.UUID(payload.get('sub'))
  
  if not (user_data := await user_repo.get_by_uid(user_id)):
    raise UserNotFoundError(user_id)
  return user_data


def require_roles(allowed_roles: List[RoleBase]):
  def role_checker( current_user: Annotated[UserModel, Depends(get_current_user)])-> UserModel:
    if current_user.role not in allowed_roles:
      raise AuthorizationError
    return current_user
  return role_checker











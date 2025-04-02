import uuid
from typing import  Any,List
from datetime import datetime, timezone, timedelta


from passlib.context import CryptContext
from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError, ExpiredSignatureError 
from pydantic import EmailStr,ValidationError

from ..db.models import UserModel
from ..core.config import setting
from ..schema.auth import CreateIUserDict, CreateUser, UserLogin
from ..exceptions.auth import PydanticException, AuthenticateEx, InvalidPasswordError,JWTEx

#? hash and verify password
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password_utils(password: str) -> str:
  return pwd.hash(password)
def verify_password_utils(plain_password: str, hash_password: str) -> bool:
  return pwd.verify(plain_password, hash_password)


#? error response schema
def error_schema(body: str, field: str):
  return {
    "type": "UniqueViolation",
    "loc": [ body],
    "msg": f"{body} already exists",
    "input": field
  }


#? user repository
class UserRepositoryUtils:
  def __init__(self, db: AsyncSession):
    self.db = db
    self.model = UserModel
  async def _statement(self,  field: str, value: Any):
    statement = (
      select(self.model).where(getattr(self.model, field) == value)
    )
    
    result = await self.db.execute(statement)
    user =  result.scalars().first()
    return user
  async def get_by_email(self, email: EmailStr) -> UserModel:
    return await self._statement("email", email)
  
  async def get_by_username(self, username: str) -> UserModel:
    return await self._statement("username", username)
  
  async def get_by_uid(self, uid: uuid.UUID) -> UserModel:
    return await self._statement("uid", uid)

  async def create(self, **kwargs):
    new_user = self.model(**kwargs)
    self.db.add(new_user)
    await self.db.commit()
    await self.db.refresh(new_user)
    return new_user


#? create token
async def create_token(token_dict: dict ,response: Response):
  current_time= datetime.now(timezone.utc)
  expires_delta = timedelta(days=setting.ACCESS_TOKEN_EXPIRE_DAYS)
  expire = current_time + expires_delta if expires_delta else current_time + timedelta(days=7)
  to_encod = token_dict.copy()
  to_encod.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encod, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

  response.set_cookie(
    key="access_token",
    value= encoded_jwt,
    httponly=True,
    secure=False,  # Added secure flag for HTTPS
    samesite='lax',  # Added samesite protection
    path="/",  # Ensure cookie is accessible across your domain
    max_age=60 * 60 * 24 * 15  # 7 days (in seconds)
  )


#? decode jwt token
def jwt_decode(token: str, options: dict | None = None):
  try:
    payload = jwt.decode( token, setting.SECRET_KEY, algorithms=setting.ALGORITHM, options=options if options else {},)
    return payload
  except (ExpiredSignatureError,JWTError) as e:
    raise JWTEx(detail=str(e))



#! register utils
async def unique_validation(db: AsyncSession,email: EmailStr, username: str) -> List[dict]:
  """* a private methods that are used to validate the uniqueness of the email and username """
  user_repo = UserRepositoryUtils(db)
  errors = []
  if existing_username :=  await user_repo.get_by_username(username):
    errors.append(error_schema("username", existing_username.username))
  if existing_email := await user_repo.get_by_email(email):
    errors.append(error_schema("email", existing_email.email))
  return errors

async def validate_user_data(db: AsyncSession,user: CreateIUserDict) -> CreateUser:
  errors = []
  result = None
  try:
    user_data = CreateUser(**user.model_dump())
  except ValidationError as pe:
    errors.extend(pe.errors())
  else:
    result = user_data

  if unique_errors := await unique_validation(db, user.email, user.username):
    errors.extend(unique_errors)

  if errors:
    raise PydanticException(errors)

  return result


#! login urils
async def authenticate_user(repo: UserRepositoryUtils,form_data: UserLogin ) -> UserModel:
  
  user = await repo.get_by_email(form_data.email)

  if not user:
    raise AuthenticateEx
  
  if form_data.password != user.password:
    if not verify_password_utils(form_data.password, user.password):
      raise InvalidPasswordError
  
  return user

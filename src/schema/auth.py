from datetime import datetime, date
from importlib.metadata import requires
from operator import le
from fastapi import Form
from pydantic import BaseModel, Field, ConfigDict, EmailStr, StrictStr,field_validator
import uuid
from enum import Enum, StrEnum
from typing import List,Optional


class Order(StrEnum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(StrEnum):
  USERNAME='username'
  ROLE='role'
  LAST_LOGIN_DATE='last_login_date'
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"

class RoleBase(StrEnum):
  USER = "user"
  ADMIN = "admin"
  ACCOUNTANT = "accountant"
  STOCK_KIPPER = "stock_kipper"
  MANAGER = "manager"


class UserBase(BaseModel):
  username: StrictStr = Field(...,max_length=128)
  email: EmailStr
  
  model_config = ConfigDict(str_strip_whitespace=True)


class GetFullUser(UserBase):
  uid: uuid.UUID | None = None
  role: str
  is_active: bool
  last_login_date: datetime | None = None
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(str_strip_whitespace=True,)


class CreateIUserDict(BaseModel):
  username: str | None = None
  email: str | None = None
  password: str | None = None

  model_config = ConfigDict(str_strip_whitespace=True,)

class AdminCreateIUserDict(BaseModel):
  username: str | None = None
  email: str | None = None
  password: str | None = None
  role: Optional[RoleBase] = None

  @field_validator("role", mode="before")
  @classmethod
  def empty_string_to_none(cls, v):
    if v == "":
      return None
    return v

  model_config = ConfigDict(str_strip_whitespace=True,)

class CreateUser(UserBase):
  password: str = Field(min_length=8, max_length=128)

  model_config = ConfigDict(str_strip_whitespace=True,extra='forbid',)


class UserLogin(BaseModel):
  email: str
  password: str 

  @field_validator("email")
  @classmethod
  def validate_email(cls, value):
    if not value.strip():
      raise ValueError("Email are required")
    try:
      EmailStr._validate(value)
    except ValueError as ex:
      raise ValueError(str(ex))
    return value

  @field_validator("password")
  @classmethod
  def validate_password(cls, value):
    if not value.strip():
      raise ValueError("Password are required")
    return value
  
  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

class UpdateUserSchema(AdminCreateIUserDict):
  pass



class GetBySchema(BaseModel):
  username: str | None = None
  email: str | None = None
  role: RoleBase | None = None








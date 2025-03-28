from datetime import datetime, date
from importlib.metadata import requires
from operator import le
from fastapi import Form
from pydantic import BaseModel, Field, ConfigDict, EmailStr, StrictStr,field_validator
import uuid
from enum import Enum
from typing import List,Optional



class RoleBase(str, Enum):
  user = "user"
  admin = "admin"
  accountant = "accountant"
  stock_kipper = "stock_kipper"



class UserBase(BaseModel):
  username: StrictStr = Field(...,max_length=128)
  email: EmailStr
  
  model_config = ConfigDict(str_strip_whitespace=True)


class GetFullUser(UserBase):
  uid: uuid.UUID
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












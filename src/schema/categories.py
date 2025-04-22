import  enum
from unittest.mock import Base
import uuid
from typing import List, Optional
from datetime import  datetime

from pydantic import BaseModel, ConfigDict,field_validator

from .items import ItemCategoryRes, ItemsBaseSchema

class Order(enum.Enum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(enum.Enum):
  NAME  = "name"
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"

class BaseCategoriesSchema(BaseModel):
  name: str

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )
  @field_validator("name")
  @classmethod
  def validate_name(cls, value):
    if not value.strip():
      raise ValueError("Name are required")
    return value

class CategoriesTime(BaseModel):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class UserModelSchema(BaseModel):
  username: str


class CategoriesItemMainSchema(BaseCategoriesSchema,CategoriesTime):
  uid: uuid.UUID | None = None
  user_uid: uuid.UUID
  
  user_model: Optional[UserModelSchema]
  
class CategoriesItemSchema(CategoriesItemMainSchema):
  items_model: List[ItemCategoryRes] = []



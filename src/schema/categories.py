import  enum
import uuid
from typing import List
from datetime import  datetime

from pydantic import BaseModel, ConfigDict

from .items import ItemsBaseSchema

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


class CategoriesTime(BaseModel):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class CategoriesItemSchema(BaseCategoriesSchema,CategoriesTime):
  uid: uuid.UUID | None = None
  user_uid: uuid.UUID

  items_model: List[ItemsBaseSchema] = []



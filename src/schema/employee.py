import  enum
import uuid
from typing import List
from datetime import  datetime

from pydantic import BaseModel, ConfigDict



class Order(enum.Enum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(enum.Enum):
  NAME  = "name"
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"

class BaseEmployeeSchema(BaseModel):
  name: str

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class TimeSchema(BaseModel):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class  EmployeeWithInfoSchema(BaseEmployeeSchema,TimeSchema):
  uid: uuid.UUID
  pass

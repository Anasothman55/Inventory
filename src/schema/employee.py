import  enum
import uuid
from typing import List, Any
from datetime import  datetime

from pydantic import BaseModel, ConfigDict

from .item_transactions import GetFullTransactions1, BaseTransactions, GetFullEmployeeWithTransactions

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

class  EmployeeFullSchema(BaseEmployeeSchema,TimeSchema):
  uid: uuid.UUID


class  EmployeeWithUseSchema(BaseEmployeeSchema,TimeSchema):
  uid: uuid.UUID
  item_transaction_model_em: List[GetFullEmployeeWithTransactions] = []


class  EmployeeWithInfoSchema(BaseEmployeeSchema,TimeSchema):
  uid: uuid.UUID


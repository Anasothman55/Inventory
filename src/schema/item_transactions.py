from datetime import date, time, datetime, timezone
import uuid
import enum
from typing import  Optional

from pydantic import BaseModel,Field, ConfigDict, field_validator



class Order(enum.Enum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(enum.Enum):
  QUANTITY  = "quantity"
  ACTION_TYPE = "action_type"
  TRANSACTION_DATE = "transaction_date"
  TRANSACTION_TIME = "transaction_time"
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"



def get_current_time() -> datetime:
  return datetime.now()
def get_date() -> date:
  return get_current_time().date()
def get_time()-> time:
  return get_current_time().time()


class EmployeeName(BaseModel):
  name: str

class EmployeeNameWithUid(BaseModel):
  uid: uuid.UUID
  name: str

class ItemName(BaseModel):
  item_name: str



class ActionType(enum.StrEnum):
  USE = 'use'
  RETURN = 'return'

class BaseTransactions(BaseModel):
  quantity: int = Field(...,gt=0,)
  action_type: ActionType

class CreateTransactions(BaseTransactions):
  transaction_date: date = Field(default_factory=get_date)
  transaction_time: time = Field(default_factory=get_time)
  note: str | None = None
  employee_uid: uuid.UUID

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

class UpdateTransactions(BaseModel):
  quantity: int = Field(None,gt=0,)
  transaction_date: date | None = None
  transaction_time: time | None = None
  note: str | None = None

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

  @field_validator("transaction_date", mode="before")
  @classmethod
  def empty_string_to_none2(cls, v):
    if v == "":
      return None
    return v

  @field_validator("transaction_time", mode="before")
  @classmethod
  def empty_string_to_none3(cls, v):
    if v == "":
      return None
    return v

class TimeSchema(BaseModel):
  created_at: datetime
  updated_at: datetime


class GetFullTransactions1(BaseTransactions,TimeSchema):
  uid: uuid.UUID
  transaction_date: date = Field(default_factory=get_date)
  transaction_time: time = Field(default_factory=get_time)
  note: str | None = None

class GetFullTransactions2(CreateTransactions,TimeSchema):
  uid: uuid.UUID
  employee_model: EmployeeName
  items_model: ItemName

class GetFullEmployeeWithTransactions(GetFullTransactions1):
  items_model: ItemName

class GetFullItemsWithTransactions(GetFullTransactions1):
  employee_model: EmployeeNameWithUid


class GetBySchema(BaseModel):
  quantity: int | None = None
  transaction_date: date | None = None
  transaction_time: time | None = None

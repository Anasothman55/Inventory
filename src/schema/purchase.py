import uuid
import enum
from typing import List
from datetime import datetime,date
from decimal import Decimal

from pydantic import  BaseModel,ConfigDict, Field

from .purchase_items import  BasePurchaseItemSchema, GetFullPurchaseItemsSchema

class Curuncy(enum.Enum):
  USD  = "USD"
  dinar = "dinar"


class Order(enum.Enum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(enum.Enum):
  PURCHASER  = "purchaser"
  TOTAL_PRICE = "total_price"
  PURCHASE_DATE = "purchase_date"
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"


class BasePurchaseSchema(BaseModel):
  purchasing_plase : str | None  = None
  purchaser : str | None  = None
  beneficiary: str | None  = None
  curuncy_type: str | None  = None
  total_price: Decimal | None  = None

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class BasePurchaseSchema2(BasePurchaseSchema):
  receipt_number : int | None = None
  recipient: str | None = None
  note : str | None = None
  purchase_date : date | None = None

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

class CreatePurchaseSchema(BaseModel):
  purchasing_plase : str = Field(...)
  purchaser : str | None  = None
  beneficiary : str = Field(...)
  curuncy_type: Curuncy = Field(...)
  total_price: Decimal = Field(...)
  receipt_number : int | None = None
  recipient: str = Field(...)
  note : str | None = None
  purchase_date : date | None = None

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

class UpdatePurchaseSchema(BasePurchaseSchema2):
  pass

class GetFullPurchaseSchema(BasePurchaseSchema2):
  uid : uuid.UUID  | None = None
  user_uid : uuid.UUID  | None = None
  created_at: datetime
  updated_at: datetime


class GetPurchaseItemsSchema(GetFullPurchaseSchema):
  purchas_items_model : List[GetFullPurchaseItemsSchema]







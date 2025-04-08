import uuid
import enum
from typing import List
from datetime import datetime


from pydantic import  BaseModel, ConfigDict

from .purchase_items import  BasePurchaseItemSchema
from .item_transactions import GetFullItemsWithTransactions

class Order(enum.Enum):
  DESC  = "desc"
  ASC  = "asc"

class OrderBy(enum.Enum):
  NAME  = "item_name"
  STOCK = "stock"
  MSL = "minimum_stock_level"
  CREATED_AT = "created_at"
  UPDATED_AT = "updated_at"


class ItemsBaseSchema(BaseModel):
  item_name : str
  stock : int
  unit : str
  minimum_stock_level : int | None = None

class ItemsBasicSchema(BaseModel):
  uid: uuid.UUID | None = None
  item_name : str

class CreateItemSchema(ItemsBaseSchema):
  description: str | None = None
  category_uid: uuid.UUID

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class UpdateItemSchema(ItemsBaseSchema):
  item_name : str | None = None
  stock : int | None = None
  unit : str | None = None
  minimum_stock_level : int | None = None
  description: str | None = None

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class ItemFullSchema(ItemsBaseSchema):
  uid: uuid.UUID
  description: str
  category_uid: uuid.UUID
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )


class GetItemFullJoin(ItemFullSchema):
  purchas_items_model: List[BasePurchaseItemSchema] = []
  item_transaction_model: List[GetFullItemsWithTransactions] = []
import uuid
import enum
from typing import List, Optional
from datetime import datetime


from pydantic import  BaseModel, ConfigDict, field_validator

from .purchase_items import  BasePurchaseItemSchema2
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

class ItemCategoryRes(ItemsBaseSchema):
  uid: uuid.UUID

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
  @field_validator("minimum_stock_level", mode="before")
  @classmethod
  def empty_string_to_none1(cls, v):
    if v == "" or None:
      return None
    if int(v) < 0:
      raise ValueError("minimum_stock_level must be greater than or equal to 0")
    return v

  @field_validator("stock", mode="before")
  @classmethod
  def empty_string_to_none2(cls, v):
    if v == "" or None:
      return None
    if int(v) < 0:
      raise ValueError("stock must be greater than or equal to 0")
    return v

  @field_validator("unit", mode="before")
  @classmethod
  def empty_string_to_none3(cls, v):
    if v.strip() == "" or v == None:
      return None
    return v

  @field_validator("item_name", mode="before")
  @classmethod
  def empty_string_to_none4(cls, v):
    if v.strip() == "" or v == None:
      return None
    return v

class UpdateItemSchema(BaseModel):
  item_name : str | None = None
  stock : int | None = None
  unit : str | None = None
  minimum_stock_level : int | None = None
  description: str | None = None
  category_uid: uuid.UUID
  model_config = ConfigDict(
    extra='forbid',
    str_strip_whitespace=True
  )

  @field_validator("minimum_stock_level", mode="before")
  @classmethod
  def empty_string_to_none1(cls, v):
    if v == "" or None:
      return None
    if int(v) < 0:
      raise ValueError("minimum_stock_level must be greater than or equal to 0")
    return v

  @field_validator("stock", mode="before")
  @classmethod
  def empty_string_to_none2(cls, v):
    if v == "" or None:
      return None
    if int(v) < 0:
      raise ValueError("stock must be greater than or equal to 0")
    return v

  @field_validator("unit", mode="before")
  @classmethod
  def empty_string_to_none3(cls, v):
    if v.strip() == "" or v == None:
      return None
    return v

  @field_validator("item_name", mode="before")
  @classmethod
  def empty_string_to_none4(cls, v):
    if v.strip() == "" or v == None:
      return None
    return v

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


class UserModelSchema(BaseModel):
  username: str

class CategoryNameModel(BaseModel):
  name: str

class GetItemFullJoin(ItemFullSchema):
  purchas_items_model: List[BasePurchaseItemSchema2] = []
  item_transaction_model: List[GetFullItemsWithTransactions] = []
  category_model : Optional[CategoryNameModel] = None
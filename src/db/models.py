
from sqlalchemy import Column, TIMESTAMP, DateTime,Date, false
from sqlmodel import  SQLModel,Field, Relationship,DECIMAL, Date
from sqlalchemy.sql import func
import sqlalchemy.dialects.postgresql as pg

import uuid
from datetime import datetime, timezone, date
from typing import List, Optional
from decimal import Decimal


def get_current_time():
  return datetime.now(timezone.utc)


class UserModel(SQLModel, table= True):
  __tablename__ = "users"

  uid: uuid.UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), primary_key=True,index=True, unique=True, default=uuid.uuid4))

  username: str = Field(unique=True, index=True)
  email: str = Field(unique=True, index=True)
  role: str = Field(index= True, default="user")
  is_active: bool = Field(default=True)
  password: str = Field(exclude=True, nullable=True)
  last_login_date: datetime = Field(sa_column=Column( DateTime(timezone=True), nullable=True ))

  created_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_current_time))

  def __repr__(self):
    return f"<Book {self.username}>"



class CategoryModel(SQLModel, table = True):
  __tablename__ = "categories"

  uid: uuid.UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), primary_key=True,index=True, unique=True, default=uuid.uuid4))

  name: str = Field(index=True, unique= True)

  user_uid: uuid.UUID = Field( foreign_key="users.uid")

  items_model: List["ItemsModel"] = Relationship(back_populates="category_model",sa_relationship_kwargs={"lazy": "selectin"})

  created_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_current_time))

  def __repr__(self):
    return f"<Book {self.name}>"




class ItemsModel(SQLModel , table= True):
  __tablename__ = "items"

  uid: uuid.UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), primary_key=True,index=True, unique=True, default=uuid.uuid4))

  item_name: str = Field(unique=True, index=True)
  stock: int = Field(default=0, index=True, ge=0)
  unit: str = Field(index=True, default="pices")
  minimum_stock_level: int = Field(index=True , default=0, ge=0)
  description : str = Field(index=True, default="")
  
  user_uid: uuid.UUID = Field( foreign_key="users.uid")
  category_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="categories.uid")
  
  purchas_items_model: List["PurchaseItemsModel"] = Relationship(back_populates="items_model",sa_relationship_kwargs={"lazy": "selectin"})
  category_model: Optional[CategoryModel] = Relationship(back_populates="items_model", sa_relationship_kwargs={"lazy": "selectin"})

  created_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_current_time))

  def __repr__(self):
    return f"<Book {self.item_name}>"


class PurchaseModel(SQLModel, table= True):
  __tablename__ = "purchase"

  uid: uuid.UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), primary_key=True,index=True, unique=True, default=uuid.uuid4))

  purchasing_plase: str = Field(index=True, nullable=True)
  purchaser: str = Field(index=True, nullable=True, max_length=128)
  beneficiary: str = Field(index=True, nullable=True, max_length= 128)
  curuncy_type: str = Field(index=True, default='dinar')
  total_price: Decimal = Field(sa_column=Column(DECIMAL(10, 2), default=0.0))
  receipt_number: int = Field(index=True, nullable=True)
  recipient: str = Field(index=True, nullable=False)
  note: str = Field(index=True, nullable=True)
  purchase_date: date = Field(sa_column=Column(Date, nullable=True))  # Corrected
  user_uid: uuid.UUID = Field( foreign_key="users.uid")
  
  purchas_items_model: List["PurchaseItemsModel"] = Relationship(back_populates="purchas_model",sa_relationship_kwargs={"lazy": "selectin"})

  created_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_current_time))

  def __repr__(self):
    return f"<Book {self.purchaser}>"




class PurchaseItemsModel(SQLModel, table= True):
  __tablename__ = "purchas_items"

  uid: uuid.UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), primary_key=True,index=True, unique=True, default=uuid.uuid4))

  quantity: int = Field(gt=0, nullable=False)
  unite_price: Decimal = Field(sa_column=Column(DECIMAL(10, 2), default=0.0))
  subtotal_price : Decimal = Field(sa_column=Column(DECIMAL(11, 2), default=0.0))
  note: str = Field(index=True, nullable=True)
  
  user_uid: uuid.UUID = Field( foreign_key="users.uid")
  item_uid: uuid.UUID = Field(foreign_key="items.uid")
  purchas_uid: uuid.UUID = Field(foreign_key="purchase.uid")
  
  purchas_model: Optional[PurchaseModel] = Relationship(back_populates="purchas_items_model", sa_relationship_kwargs={"lazy": "selectin"})
  items_model: Optional[ItemsModel] = Relationship(back_populates="purchas_items_model", sa_relationship_kwargs={"lazy": "selectin"})

  created_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_current_time,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_current_time))

def __repr__(self):
    return f"<Book {self.uid}>"
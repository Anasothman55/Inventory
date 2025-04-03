from fastapi import Depends

from ..db.index import get_db
from ..db.models import PurchaseItemsModel,ItemsModel
from ..schema.categories import Order, OrderBy
from .items import ItemsRepository

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,desc, asc

from decimal import Decimal
from typing import Any, Annotated, Callable
import uuid

class PurchasesItemsRepository:
  def __init__(self, db):
    self.db = db
    self.model = PurchaseItemsModel

  async def _statement(self, field: str, value: Any):
    statement = select(self.model).where(getattr(self.model, field) == value)
    result = await self.db.execute(statement)
    return result.scalars().first()

  async def _commit_refresh(self, row):
    await self.db.commit()
    await self.db.refresh(row)
    return row

  async def delete_row(self, row):
    await self.db.delete(row)
    await self.db.commit()


  async def get_by_uid(self, uid: uuid.UUID):
    return await self._statement(field="uid", value=uid)

  async def get_by_quantity(self, quantity: int):
    return await self._statement(field="quantity", value=quantity)

  async def get_by_unite_price(self, unite_price: Decimal):
    return await self._statement(field="unite_price", value=unite_price)

  async def get_by_subtotal_price(self, subtotal_price: Decimal):
    return await self._statement(field="subtotal_price", value= subtotal_price)

  async def get_all(self, order: Order, order_by: OrderBy):
    order_column = getattr(self.model, order_by.value )

    if order.value == "desc": order_column = desc(order_column)
    else: order_column = asc(order_column)

    statement = (select(self.model).order_by(order_column))
    result = await self.db.execute(statement)
    return result.scalars().all()

  async def create_row(self,new_row) -> PurchaseItemsModel:
    self.db.add(new_row)
    return await self._commit_refresh(new_row)

  async def update_row(self, req_data:dict, row_model: PurchaseItemsModel) -> PurchaseItemsModel:
    for key, value in req_data.items():
      if value:
        setattr(row_model,key,value)
    return await self._commit_refresh(row_model)

async def get_purchases_items_repo(db: Annotated[AsyncSession, Depends(get_db)]):
  return PurchasesItemsRepository(db)



async def create_new_row_utils(
    data: dict, create_row: Callable, update_row: Callable, items: ItemsModel):
  new_row = PurchaseItemsModel(**data)
  new_data = await create_row(new_row)
  new_stock = new_data.quantity + items.stock
  item_update_dict = {"stock": new_stock}
  await update_row(item_update_dict, items)

  return new_data



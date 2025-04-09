from fastapi import Depends
from sqlalchemy import Select

from .items import ItemsRepository
from ..db.index import get_db
from ..db.models import ItemsModel, ItemTransactions
from ..schema.item_transactions import Order, OrderBy, GetBySchema, ActionType
from ..exceptions.item_transactions import TransactionsStock

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select , desc, asc

from datetime import date, time
from typing import Any, Annotated, Callable
import uuid

class ItemTransactionsRepository:
  def __init__(self, db):
    self.db = db
    self.model = ItemTransactions

  async def _statement(self, field: str, value: Any):
    statement = select(self.model).options(
      selectinload(self.model.items_model)
    ).where(getattr(self.model, field) == value)
    result = await self.db.execute(statement)
    return result.scalars().first()

  async def _commit_refresh(self, row):
    await self.db.commit()
    await self.db.refresh(row)
    return row

  async def delete_row(self, row):
    await self.db.delete(row)
    await self.db.commit()


  async def get_by_uid(self, uid: uuid.UUID)-> ItemTransactions:
    return await self._statement(field="uid", value=uid)

  async def get_by_quantity(self, quantity: int):
    return await self._statement(field="quantity", value=quantity)

  async def get_by_action_type(self, action_type: str):
    return await self._statement(field="action_type", value=action_type)

  async def get_by_transaction_date(self, transaction_date: date):
    return await self._statement(field="transaction_date", value= transaction_date)

  async def get_by_transaction_time(self, transaction_time: time):
    return await self._statement(field="transaction_time", value= transaction_time)

  async def get_all(self, order: Order, order_by: OrderBy,filters: GetBySchema):
    order_column = getattr(self.model, order_by.value )

    if order.value == "desc": order_column = desc(order_column)
    else: order_column = asc(order_column)

    statement: Select = select(self.model)

    # Dynamically apply filters
    for field_name, value in filters.model_dump(exclude_none=True).items():
      if hasattr(self.model, field_name):
        statement = statement.where(getattr(self.model, field_name) == value)

    # Apply ordering
    statement = statement.order_by(order_column)

    result = await self.db.execute(statement)
    return result.scalars().all()
  async def create_row(self,new_row) -> ItemTransactions:
    self.db.add(new_row)
    return await self._commit_refresh(new_row)

  async def update_row(self, req_data:dict, row_model: ItemTransactions) -> ItemTransactions:
    for key, value in req_data.items():
      if value:
        setattr(row_model,key,value)
    return await self._commit_refresh(row_model)

async def get_items_transactions_repo(db: Annotated[AsyncSession, Depends(get_db)]):
  return ItemTransactionsRepository(db)


async def update_items_by_transactions(
    items_repo: ItemsRepository,
    items: ItemsModel,
    qty: int
):
  item_update_dict = {"stock": qty}
  await items_repo.update_row(item_update_dict, items)


def update_transactions_utils(
    stock: int,
    abc_qty: int,
    new_qty: int,
    old_qty: int,
    actions: str
):

  if actions == ActionType.USE:
    if new_qty > stock + old_qty:
      raise TransactionsStock
    if old_qty > new_qty:
      stock += abc_qty
    else:
      stock -= abc_qty
  else:
    if old_qty > new_qty:
      stock -= abc_qty
    else:
      stock += abc_qty

  return stock

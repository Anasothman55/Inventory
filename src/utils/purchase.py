from fastapi import Depends

from ..db.index import get_db
from ..db.models import PurchaseModel
from ..schema.purchase import Order, OrderBy,CreatePurchaseSchema
from ..exceptions.purchase import PurchaseAlreadyExists

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,desc, asc

from datetime import date
from typing import Any, Annotated
import uuid

class PurchasesRepository:
  def __init__(self, db):
    self.db = db
    self.model = PurchaseModel

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

  async def get_by_purchasing_plase(self, name: str) -> PurchaseModel:
    return await self._statement(field="purchasing_plase", value=name)

  async def get_by_purchaser(self, unit: str):
    return await self._statement(field="purchaser", value=unit)

  async def get_by_curuncy_type(self, uid: uuid.UUID):
    return await self._statement(field="curuncy_type", value= uid)

  async def get_by_receipt_number(self, rn: int):
    return await self._statement(field="receipt_number", value= rn)

  async def get_by_recipient(self, uid: uuid.UUID):
    return await self._statement(field="recipient", value= uid)

  async def get_all(self, order: Order, order_by: OrderBy):
    order_column = getattr(self.model, order_by.value )

    if order.value == "desc": order_column = desc(order_column)
    else: order_column = asc(order_column)

    statement = (
      select(self.model).options(selectinload(self.model.purchas_items_model)).order_by(order_column)
    )
    result = await self.db.execute(statement)
    return result.scalars().all()

  async def create_row(self,new_row) -> PurchaseModel:
    self.db.add(new_row)
    return await self._commit_refresh(new_row)

  async def update_row(self, req_data:dict, row_model: PurchaseModel) -> PurchaseModel:
    for key, value in req_data.items():
      if value:
        setattr(row_model,key,value)
    return await self._commit_refresh(row_model)

async def get_purchases_repo(db: Annotated[AsyncSession, Depends(get_db)]):
  return PurchasesRepository(db)



async def check_purchase_unique(
    repo: PurchasesRepository, purchasing_plase: str ,receipt_number: int ):
  existing_purchase  = await repo.get_by_purchasing_plase(purchasing_plase)
  if existing_purchase and existing_purchase.receipt_number == receipt_number:
    raise PurchaseAlreadyExists(existing_purchase.purchasing_plase, existing_purchase.receipt_number)






from fastapi import Depends

from ..db.index import get_db
from ..db.models import EmployeeModel
from ..schema.employee import Order, OrderBy

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,desc, asc
from typing import Any, Annotated
import uuid

class EmployeeRepository:
  def __init__(self, db):
    self.db = db
    self.model = EmployeeModel

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

  async def get_by_name(self, name: str):
    return await self._statement(field="name", value=name)

  async def get_all(self, order: Order, order_by: OrderBy):
    order_column = getattr(self.model, order_by.value )

    if order.value == "desc":
      order_column = desc(order_column)
    else:
      order_column = asc(order_column)

    statement = (
      select(self.model).options(
        selectinload(self.model.employee_info_model),
                selectinload(self.model.item_transaction_model_em)
      ).order_by(order_column)
    )
    result = await self.db.execute(statement)
    return result.scalars().all()

  async def create_row(self,new_row) -> EmployeeModel:
    self.db.add(new_row)
    return await self._commit_refresh(new_row)

  async def update_row(self, req_data:dict, row_model: EmployeeModel) -> EmployeeModel:
    for key, value in req_data.items():
      if value:
        setattr(row_model,key,value)
    return await self._commit_refresh(row_model)

async def get_employee_repo(db: Annotated[AsyncSession, Depends(get_db)]):
  return EmployeeRepository(db)










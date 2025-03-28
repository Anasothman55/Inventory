from sqlalchemy.ext.asyncio import  AsyncSession
from sqlmodel import select

import uuid
from typing import Any

from ..db.models import ItemsModel


class ItemsRepositoryUtils:
  def __init__(self, db: AsyncSession):
    self.db = db
    self.model = ItemsModel
  async def _statement(self,  field: str, value: Any):
    statement = (
      select(self.model).where(getattr(self.model, field) == value)
    )

    result = await self.db.execute(statement)
    user =  result.scalars().first()
    return user

  async def get_by_username(self, username: str) -> ItemsModel:
    return await self._statement("username", username)

  async def get_by_uid(self, uid: uuid.UUID) -> ItemsModel:
    return await self._statement("uid", uid)

  async def create(self, **kwargs):
    new_user = self.model(**kwargs)
    self.db.add(new_user)
    await self.db.commit()
    await self.db.refresh(new_user)
    return new_user

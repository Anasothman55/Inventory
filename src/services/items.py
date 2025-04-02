
import  uuid

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


from ..db.models import ItemsModel
from ..utils.items import ItemsRepository
from ..schema.items import CreateItemSchema, UpdateItemSchema
from ..exceptions.Items import ItemsAlreadyExists, ItemsNotFound

async def create_items_services(
    user_uid:uuid.UUID,
    repo: ItemsRepository,
    req_data:CreateItemSchema) -> ItemsModel :
  try:
    new_data = req_data.model_dump()
    new_data.update({"user_uid": user_uid})

    new_row = ItemsModel(**new_data )
    result = await repo.create_row(new_row)
    return result
  except IntegrityError as e:
    raise ItemsAlreadyExists(req_data.item_name)


async def get_one_items_services(repo: ItemsRepository, uid: uuid.UUID) -> ItemsModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise ItemsNotFound(uid)
  return result




async def update_items_services(
    repo: ItemsRepository,
    uid: uuid.UUID,
    new_data: UpdateItemSchema) -> ItemsModel:
  item = await get_one_items_services(repo,uid)
  result = await repo.update_row(new_data.model_dump(), item)
  return result


async def delete_items_services(repo: ItemsRepository, uid: uuid.UUID) -> None:
  item = await get_one_items_services(repo,uid)
  await repo.delete_row(item)
  return None













from fastapi import Depends, HTTPException, Response, status

from sqlalchemy.exc import IntegrityError

import uuid

from rich import print

from ..db.index import get_db
from ..db.models import CategoryModel
from ..utils.categories import CategoryRepository
from ..schema.categories import BaseCategoriesSchema




async def create_category_services(
    user_uid:uuid.UUID,
    repo: CategoryRepository,
    req_data:BaseCategoriesSchema) -> CategoryModel:

  try:
    new_data = req_data.model_dump()
    new_data.update({"user_uid": user_uid})

    new_row = CategoryModel(**new_data )
    result = await repo.create_row(new_row)
    return result
  except IntegrityError as e:
    print(f"IntegrityError: {e}")
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="Categories already exists"
    )

async def get_one_category_services(repo: CategoryRepository, uid: uuid.UUID) -> CategoryModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Category not found"
    )
  return result


async def update_category_services(
    repo: CategoryRepository,
    uid: uuid.UUID, req_data: BaseCategoriesSchema) -> CategoryModel:
  category = await get_one_category_services(repo,uid)
  result = await repo.update_row(req_data.model_dump(), category)
  return result


async def delete_category_services(repo: CategoryRepository, uid: uuid.UUID) -> None:
  category = await repo.get_by_uid(uid)
  await repo.delete_row(category)
  return None
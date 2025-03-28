from rich import  print

from typing import Annotated, List
from fastapi import APIRouter,  Query, status, HTTPException, Form, Depends, Path

import uuid

from ..utils.categories import CategoryRepository,get_category_repo
from ..db.models import UserModel
from ..dependencies.auth import get_current_user
from ..schema.categories import  Order, CategoriesItemSchema,BaseCategoriesSchema,OrderBy
from ..services.categories import (
  create_category_services,
  get_one_category_services,
  update_category_services,
  delete_category_services
)





route = APIRouter(
  dependencies= [Depends(get_current_user)],
  tags=["categories"]
)


@route.get('/', response_model= List[CategoriesItemSchema], status_code= status.HTTP_200_OK)
async def get_all_categories(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
    order_by: Annotated[OrderBy, Query()] = OrderBy.CREATED_AT,
    order: Annotated[Order, Query()] = Order.ASC,
):
  res = await repo.get_all(order,order_by)
  return res


@route.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    req_data: Annotated[BaseCategoriesSchema, Form()],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
  result = await create_category_services(current_user.uid,repo,req_data)
  return result


@route.get('/{uid}',  status_code= status.HTTP_200_OK, response_model=CategoriesItemSchema)
async def get_one_categories(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
    uid: Annotated[uuid.UUID, Path(...)]
):
  result = await get_one_category_services(repo,uid)
  return result


@route.patch("/{uid}", status_code=status.HTTP_200_OK)
async def update_category(
    uid: Annotated[uuid.UUID,Path(...)],
    new_data: Annotated[BaseCategoriesSchema, Form()],
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
  result = await update_category_services(repo, uid, new_data)
  return result

@route.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    uid: Annotated[uuid.UUID, Path(...)],
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
  await delete_category_services(repo, uid)
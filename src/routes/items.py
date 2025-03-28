from rich import  print

from typing import Annotated, List
from fastapi import APIRouter,  Query, status, HTTPException, Form, Depends, Path

import uuid

from ..schema.items import (
  ItemsBaseSchema,
  ItemFullSchema,
  CreateItemSchema,
  ItemsPurchaseSchema,
  OrderBy,
  Order,
  UpdateItemSchema
)
from ..db.models import UserModel
from ..dependencies.auth import get_current_user
from ..utils.items import ItemsRepository, get_items_repo
from ..services.items import (
  create_items_services,
  get_one_items_services,
  update_items_services,
  delete_category_services,
)

route = APIRouter(
  dependencies= [Depends(get_current_user)],
  tags=["Items"]
)


@route.get('/', status_code= status.HTTP_200_OK, response_model=List[ItemsPurchaseSchema])
async def get_all_items(
    repo: Annotated[ItemsRepository, Depends(get_items_repo)],
    order_by: Annotated[OrderBy, Query()] = OrderBy.CREATED_AT,
    order: Annotated[Order, Query()] = Order.ASC,
):
  res = await repo.get_all(order,order_by)
  return res


@route.post("/", status_code=status.HTTP_201_CREATED, response_model=ItemFullSchema)
async def create_items(
    req_data: Annotated[CreateItemSchema, Form()],
    current_user: Annotated[UserModel, Depends(get_current_user)],
    repo: Annotated[ItemsRepository, Depends(get_items_repo)],
):
  res = await create_items_services(current_user.uid,repo, req_data)
  return res


@route.get('/{uid}',  status_code= status.HTTP_200_OK, response_model=ItemsPurchaseSchema)
async def get_one_items(
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[ItemsRepository, Depends(get_items_repo)],
):
  res = await get_one_items_services(repo,uid)
  return res

@route.patch("/{uid}", status_code=status.HTTP_200_OK, response_model=ItemsBaseSchema)
async def update_items(
    uid: Annotated[uuid.UUID, Path()],
    new_data: Annotated[UpdateItemSchema, Form()],
    repo: Annotated[ItemsRepository, Depends(get_items_repo)],
):
  res = await update_items_services(repo,uid,new_data)
  return res

@route.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_items(
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[ItemsRepository, Depends(get_items_repo)],
):
  await delete_category_services(repo, uid)
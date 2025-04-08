from rich import  print

from typing import Annotated, List
from fastapi import APIRouter,  Query, status, HTTPException, Form, Depends, Path

import uuid


from ..schema.auth import  RoleBase
from ..schema.item_transactions import (
  CreateTransactions,
  UpdateTransactions,
  GetFullTransactions1,
  GetFullTransactions2,
  Order,
  OrderBy,
  GetBySchema
)
from ..db.models import UserModel
from ..dependencies.auth import get_current_user, require_roles
from ..utils.item_tranactions import get_items_transactions_repo, ItemTransactionsRepository
from ..utils.items import ItemsRepository, get_items_repo
from ..services.item_transactions import (
  create_item_transactions_sservice,
  get_one_transaction_service,
  update_item_transactions_sservice,
  delete_transactions_services
)


alter_role = [RoleBase.ADMIN, RoleBase.STOCK_KIPPER]
see_role = [RoleBase.ADMIN, RoleBase.ACCOUNTANT, RoleBase.MANAGER,  RoleBase.STOCK_KIPPER]

alter_role_des = f"""this route can use by all {"and ".join(alter_role)} users"""
see_role_des = f"""this route can use by all {"and ".join(see_role)} users"""
admin_des = f"""this route can use by all {RoleBase.ADMIN} users"""



route = APIRouter(
  dependencies= [Depends(require_roles(see_role))],
  tags=["Items Transactions"]
)


@route.get('/',description=see_role_des, status_code= status.HTTP_200_OK, response_model=List[GetFullTransactions2])
async def get_all_items_transactions(
    repo: Annotated[ItemTransactionsRepository, Depends(get_items_transactions_repo)],
    filters: Annotated[GetBySchema, Depends()],
    order_by: Annotated[OrderBy, Query()] = OrderBy.CREATED_AT,
    order: Annotated[Order, Query()] = Order.ASC,
):
  res = await repo.get_all(order, order_by, filters)
  return res

@route.post("/{item_uid}",description=alter_role_des, status_code=status.HTTP_201_CREATED)
async def create_items_transactions(
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))],
    repo: Annotated[ItemTransactionsRepository, Depends(get_items_transactions_repo)],
    req_data: Annotated[CreateTransactions, Form()],
    item_uid: Annotated[uuid.UUID, Path()],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
):
  res = await create_item_transactions_sservice(current_user.uid, repo, req_data, item_uid, items_repo)
  return res
@route.get('/{uid}',description=see_role_des, status_code= status.HTTP_200_OK, response_model=GetFullTransactions2)
async def get_one_items_transactions(
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[ItemTransactionsRepository, Depends(get_items_transactions_repo)],
):
  res = await get_one_transaction_service(repo, uid)
  return  res

@route.patch("/{uid}",description=alter_role_des , status_code=status.HTTP_200_OK)
async def update_items_transactions(
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))],
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[ItemTransactionsRepository, Depends(get_items_transactions_repo)],
    new_data: Annotated[UpdateTransactions, Form()],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
):
  res = await update_item_transactions_sservice(uid,repo, new_data, items_repo)
  return  res


@route.delete("/{uid}",description=alter_role_des, status_code=status.HTTP_204_NO_CONTENT)
async def delete_items_transactions(
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))],
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[ItemTransactionsRepository, Depends(get_items_transactions_repo)],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
):
  await delete_transactions_services(uid, repo, items_repo)















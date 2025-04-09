from rich import  print

from typing import Annotated, List
from fastapi import APIRouter,  Query, status, HTTPException, Form, Depends, Path

import uuid

from ..services.purchase_items import (
  create_purchase_items_service,
  get_one_purchase_items_services,
  update_purchase_items_services,
  delete_purchase_items_services,
)
from ..schema.auth import  RoleBase
from ..schema.purchase_items import (
  BasePurchaseItemSchema,
  CreatePurchaseItemsSchema,
  GetAllPurchaseItemsSchema,
  GetFullPurchaseItemsSchema,
  OrderBy,
  Order, UpdatePurchaseItemsSchema,
)
from ..db.models import UserModel
from ..dependencies.auth import get_current_user, require_roles
from ..utils.purchase import PurchasesRepository, get_purchases_repo
from ..utils.purchase_items import PurchasesItemsRepository, get_purchases_items_repo
from ..utils.items import ItemsRepository, get_items_repo



alter_role = [RoleBase.ADMIN, RoleBase.ACCOUNTANT]
see_role = [RoleBase.ADMIN, RoleBase.ACCOUNTANT, RoleBase.MANAGER]

alter_role_des = f"""this route can use by all {RoleBase.ADMIN} and { RoleBase.ACCOUNTANT} users"""
see_role_des = f"""this route can use by all {RoleBase.ADMIN} and {RoleBase.ACCOUNTANT} and {RoleBase.MANAGER} users"""
admin_des = f"""this route can use by all {RoleBase.ADMIN} users"""



route = APIRouter(
  dependencies= [Depends(require_roles(see_role))],
  tags=["Purchases Items"]
)


@route.get('/',description=see_role_des, status_code= status.HTTP_200_OK, response_model=List[GetAllPurchaseItemsSchema])
async def get_all_purchase_items(
  repo : Annotated[PurchasesItemsRepository , Depends(get_purchases_items_repo)],
  order_by: Annotated[OrderBy, Query()] = OrderBy.CREATED_AT,
  order: Annotated[Order, Query()] = Order.ASC,
):
  res = await repo.get_all(order, order_by)
  return res


@route.post("/{purchase_uid}", description=alter_role_des, status_code=status.HTTP_201_CREATED)
async def create_purchase_items(
    purchase_uid: Annotated[uuid.UUID, Path()],
    req_data: Annotated[CreatePurchaseItemsSchema , Form()],
    repo: Annotated[PurchasesItemsRepository , Depends(get_purchases_items_repo)],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))]
):
  res = await create_purchase_items_service(repo, items_repo, req_data, current_user.uid, purchase_uid)
  return res

@route.get('/{uid}',description=see_role_des, status_code= status.HTTP_200_OK, response_model=GetAllPurchaseItemsSchema)
async def get_one_purchase_items(
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[PurchasesItemsRepository , Depends(get_purchases_items_repo)],):
  res = await get_one_purchase_items_services(repo, uid)
  return res

@route.patch("/{uid}",description=alter_role_des , status_code=status.HTTP_200_OK, response_model=BasePurchaseItemSchema)
async def update_purchase_items(
    uid: Annotated[uuid.UUID, Path()],
    new_data: Annotated[UpdatePurchaseItemsSchema , Form()],
    repo: Annotated[PurchasesItemsRepository , Depends(get_purchases_items_repo)],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))]
):
  res = await update_purchase_items_services(repo,items_repo, uid, current_user.uid,new_data)
  return res

@route.delete("/{uid}",description=alter_role_des, status_code=status.HTTP_204_NO_CONTENT)
async def delete_purchase_items(
    current_user: Annotated[UserModel , Depends(require_roles(alter_role))],
    uid: Annotated[uuid.UUID, Path()],
    repo: Annotated[PurchasesItemsRepository , Depends(get_purchases_items_repo)],
    items_repo: Annotated[ItemsRepository , Depends(get_items_repo)],
):
  await delete_purchase_items_services(repo, uid,items_repo)















import uuid

from fastapi import HTTPException, status

from ..schema.purchase_items import CreatePurchaseItemsSchema
from ..schema.items import CreateItemSchema
from ..db.models import PurchaseItemsModel
from ..services.items import get_one_items_services, create_items_services
from ..utils.items import ItemsRepository
from ..utils.purchase_items import PurchasesItemsRepository, create_new_row_utils

async def create_purchase_items_service(
    repo: PurchasesItemsRepository,
    items_repo: ItemsRepository,
    req_data: CreatePurchaseItemsSchema,
    user_uid: uuid.UUID,
    purchase_uid: uuid.UUID):

  qty = req_data.quantity
  price = req_data.unite_price
  subtotal_price = qty * price

  if req_data.new_name is None and req_data.item_uid is None:
    raise HTTPException(
      status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail="You should provide items id or new name"
    )

  if req_data.item_uid:
    items_uuid = uuid.UUID(req_data.item_uid)
    items = await get_one_items_services(items_repo, items_uuid)

    data = req_data.model_dump(exclude={"new_name", "unit", "category_uid","item_uid"})
    data.update({"user_uid": user_uid, "purchas_uid":purchase_uid, "item_uid":items_uuid,"subtotal_price": subtotal_price})
    res = await create_new_row_utils(data, repo.create_row, items_repo.update_row,items)

    return res

  else :
    item_data = CreateItemSchema(
      item_name= req_data.new_name, unit= req_data.unit, category_uid= uuid.UUID(req_data.category_uid), stock= req_data.quantity)
    items = await create_items_services(user_uid, items_repo, item_data)

    data = req_data.model_dump(exclude={"item_uid"})
    data.update({"user_uid": user_uid, "purchas_uid":purchase_uid, "item_uid" : items.uid,"subtotal_price": subtotal_price})
    res = await create_new_row_utils(data, repo.create_row, items_repo.update_row,items)

    return res



async def get_one_purchase_items_services(repo: PurchasesItemsRepository, uid: uuid.UUID) -> PurchaseItemsModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Purchase info not found"
    )
  return result











import uuid

from fastapi import HTTPException, status

from ..schema.purchase_items import CreatePurchaseItemsSchema, UpdatePurchaseItemsSchema
from ..schema.items import CreateItemSchema
from ..db.models import PurchaseItemsModel
from ..services.items import get_one_items_services, create_items_services
from ..utils.items import ItemsRepository
from ..utils.purchase_items import PurchasesItemsRepository, create_new_row_utils
from ..exceptions.purchase_items import PurchaseItemsNotFound,PurchaseItemsMissingPart


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
    raise PurchaseItemsMissingPart({"name","item_uid"})

  if req_data.item_uid:
    items_uuid = uuid.UUID(req_data.item_uid)
    items = await get_one_items_services(items_repo, items_uuid)

    data = req_data.model_dump(exclude={"new_name", "unit", "category_uid","item_uid"})
    data.update({"user_uid": user_uid, "purchas_uid":purchase_uid, "item_uid":items_uuid,"subtotal_price": subtotal_price})
    res = await create_new_row_utils(data, repo.create_row, items_repo.update_row,items)

    return res

  else :
    item_data = CreateItemSchema(
      item_name= req_data.new_name, unit= req_data.unit, category_uid= uuid.UUID(req_data.category_uid), stock= 0)
    items = await create_items_services(user_uid, items_repo, item_data)

    data = req_data.model_dump(exclude={"item_uid"})
    data.update({"user_uid": user_uid, "purchas_uid":purchase_uid, "item_uid" : items.uid,"subtotal_price": subtotal_price})
    res = await create_new_row_utils(data, repo.create_row, items_repo.update_row,items)

    return res



async def get_one_purchase_items_services(repo: PurchasesItemsRepository, uid: uuid.UUID) -> PurchaseItemsModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise PurchaseItemsNotFound(uid)
  return result



async def update_purchase_items_services(
    repo: PurchasesItemsRepository,
    items_repo: ItemsRepository,
    uid: uuid.UUID,
    user_uid: uuid.UUID,
    new_req: UpdatePurchaseItemsSchema):


  pt = await get_one_purchase_items_services(repo, uid)
  old_qty = pt.quantity
  old_price = pt.unite_price
  new_qty = new_req.quantity
  new_price = new_req.unite_price

  subtotal_price = (new_price if new_price is not None else old_price) * (new_qty if new_qty is not None else old_qty)

  dumped = new_req.model_dump()
  dumped.update({"user_uid": user_uid, "subtotal_price": subtotal_price})
  res = await repo.update_row(dumped, pt)

  if pt.item_uid is not None:
    items = await get_one_items_services(items_repo, pt.item_uid)
    new_stock = items.stock + (res.quantity - old_qty)
    await items_repo.update_row({"stock": new_stock}, items)

  return res



async def delete_purchase_items_services(
    repo: PurchasesItemsRepository, uid: uuid.UUID, item_repo: ItemsRepository) -> None:
  pt = await get_one_purchase_items_services(repo,uid)
  qty = pt.quantity

  if pt.item_uid is not None:
    items = await get_one_items_services(item_repo, pt.item_uid)
    new_stock = items.stock - qty
    await item_repo.update_row({"stock": new_stock}, items)

  await repo.delete_row(pt)
  return None




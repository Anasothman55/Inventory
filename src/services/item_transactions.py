import uuid

from ..schema.item_transactions import ActionType
from ..utils.item_tranactions import ItemTransactionsRepository
from ..utils.items import ItemsRepository
from ..schema.item_transactions import CreateTransactions, UpdateTransactions
from ..services.items import get_one_items_services
from ..db.models import ItemTransactions

async def   create_item_transactions_sservice(
    user_uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    req_data: CreateTransactions,
    item_uid: uuid.UUID,
    items_repo: ItemsRepository
):

  items = await get_one_items_services(items_repo, item_uid)

  if req_data.action_type == ActionType.USE:
    if req_data.quantity > items.stock:
      raise
    used = items.stock - req_data.quantity
    item_update_dict = {"stock": used}
    await items_repo.update_row(item_update_dict, items)
  else:
    returned = items.stock + req_data.quantity
    item_update_dict = {"stock": returned}
    await items_repo.update_row(item_update_dict, items)

  new_row = ItemTransactions(**req_data.model_dump(), user_uid=user_uid, item_uid=items.uid)
  res = await repo.create_row(new_row)

  return res



async def get_one_transaction_service(
    repo: ItemTransactionsRepository,
    uid: uuid.UUID
)-> ItemTransactions:
  res = await repo.get_by_uid(uid)
  if not res:
    raise "Transaction not found"
  return res




async def update_item_transactions_sservice(
    uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    new_data: UpdateTransactions,
    items_repo: ItemsRepository
):
  transaction = await get_one_transaction_service(repo, uid)
  items = await get_one_items_services(items_repo, transaction.item_uid)

  new_qty = abs(transaction.quantity - new_data.quantity)

  if transaction.action_type == ActionType.USE:
    if new_qty > items.stock:
      raise "use must be smaller than stock item"

    if transaction.quantity > new_data.quantity:
      used =  items.stock + new_qty
    else:
      used =  items.stock - new_qty
    item_update_dict = {"stock": used}
    await items_repo.update_row(item_update_dict, items)
  else:
    if transaction.quantity > new_data.quantity:
      returned =  items.stock - new_qty
    else:
      returned =  items.stock + new_qty
    item_update_dict = {"stock": returned}
    await items_repo.update_row(item_update_dict, items)

  result = await repo.update_row(new_data.model_dump(), transaction)
  return result



async def delete_transactions_services(
    uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    items_repo: ItemsRepository
):
  transaction = await get_one_transaction_service(repo, uid)
  items = await get_one_items_services(items_repo, transaction.item_uid)

  if transaction.action_type == ActionType.USE:
    used = items.stock + transaction.quantity
    item_update_dict = {"stock": used}
    await items_repo.update_row(item_update_dict, items)
  else:
    returned = items.stock - transaction.quantity
    item_update_dict = {"stock": returned}
    await items_repo.update_row(item_update_dict, items)

  await repo.delete_row(transaction)









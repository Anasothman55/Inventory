import uuid

from ..schema.item_transactions import ActionType
from ..utils.item_tranactions import ItemTransactionsRepository,update_items_by_transactions,update_transactions_utils
from ..utils.items import ItemsRepository
from ..schema.item_transactions import CreateTransactions, UpdateTransactions
from ..services.items import get_one_items_services
from ..db.models import ItemTransactions
from ..exceptions.item_transactions import TransactionsNotFound, TransactionsStock


async def   create_item_transactions_sservice(
    user_uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    req_data: CreateTransactions,
    item_uid: uuid.UUID,
    items_repo: ItemsRepository
):

  items = await get_one_items_services(items_repo, item_uid)
  new_qty = items.stock

  if req_data.action_type == ActionType.USE:
    if req_data.quantity > items.stock:
      raise TransactionsStock
    new_qty -=  req_data.quantity
  else:
    new_qty += req_data.quantity

  await update_items_by_transactions(items_repo,items,new_qty)
  new_row = ItemTransactions(**req_data.model_dump(), user_uid=user_uid, item_uid=items.uid)
  res = await repo.create_row(new_row)

  return res



async def get_one_transaction_service(
    repo: ItemTransactionsRepository,
    uid: uuid.UUID
)-> ItemTransactions:
  res = await repo.get_by_uid(uid)
  if not res:
    raise TransactionsNotFound(uid)
  return res




async def update_item_transactions_sservice(
    uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    new_data: UpdateTransactions,
    items_repo: ItemsRepository
):
  transaction = await get_one_transaction_service(repo, uid)
  items = await get_one_items_services(items_repo, transaction.item_uid)

  abc_qty = abs(transaction.quantity - new_data.quantity)

  stock =  update_transactions_utils(items.stock, abc_qty,new_data.quantity ,transaction.quantity, transaction.action_type)

  await update_items_by_transactions(items_repo,items,stock)
  result = await repo.update_row(new_data.model_dump(), transaction)
  return result



async def delete_transactions_services(
    uid: uuid.UUID,
    repo: ItemTransactionsRepository,
    items_repo: ItemsRepository
):
  transaction = await get_one_transaction_service(repo, uid)
  items = await get_one_items_services(items_repo, transaction.item_uid)
  new_qty = items.stock

  if transaction.action_type == ActionType.USE:
    new_qty += transaction.quantity
  else:
    new_qty -= transaction.quantity

  await update_items_by_transactions(items_repo,items,new_qty)
  await repo.delete_row(transaction)









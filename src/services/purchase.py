
import  uuid

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


from ..db.models import  PurchaseModel
from ..utils.purchase import PurchasesRepository, check_purchase_unique
from ..schema.purchase import CreatePurchaseSchema, UpdatePurchaseSchema
from ..exceptions.purchase import PurchaseAlreadyExists, PurchaseNotFound



async def create_purchase_services(
    user_uid:uuid.UUID,
    repo: PurchasesRepository,
    req_data:CreatePurchaseSchema) -> PurchaseModel:
  await check_purchase_unique(repo,req_data.purchasing_plase, req_data.receipt_number)

  curuncy_type = req_data.curuncy_type.value
  new_data = req_data.model_dump(exclude={'curuncy_type'})
  new_data.update({"user_uid": user_uid, 'curuncy_type':curuncy_type})

  new_row = PurchaseModel(**new_data )
  result = await repo.create_row(new_row)
  return result


async def get_one_purchase_services(repo: PurchasesRepository, uid: uuid.UUID) -> PurchaseModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise PurchaseNotFound(uid)
  return result




async def update_purchase_services(
    repo: PurchasesRepository,
    uid: uuid.UUID,
    new_data: UpdatePurchaseSchema) -> PurchaseModel:
  purchase = await get_one_purchase_services(repo,uid)
  result = await repo.update_row(new_data.model_dump(), purchase)
  return result


async def delete_purchase_services(repo: PurchasesRepository, uid: uuid.UUID) -> None:
  purchase = await get_one_purchase_services(repo,uid)
  await repo.delete_row(purchase)
  return None

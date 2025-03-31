
import  uuid

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


from ..db.models import  PurchaseModel
from ..utils.purchase import PurchasesRepository
from ..schema.purchase import CreatePurchaseSchema, UpdatePurchaseSchema


async def create_purchase_services(
    user_uid:uuid.UUID,
    repo: PurchasesRepository,
    req_data:CreatePurchaseSchema) -> PurchaseModel:
  try:
    new_data = req_data.model_dump()
    new_data.update({"user_uid": user_uid})

    new_row = PurchaseModel(**new_data )
    result = await repo.create_row(new_row)
    return result
  except IntegrityError as e:
    print(f"IntegrityError: {e}")
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="Purchase already exists"
    )


async def get_one_purchase_services(repo: PurchasesRepository, uid: uuid.UUID) -> PurchaseModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Items not found"
    )
  return result




async def update_purchase_services(
    repo: PurchasesRepository,
    uid: uuid.UUID,
    new_data: UpdatePurchaseSchema) -> PurchaseModel:
  item = await get_one_purchase_services(repo,uid)
  result = await repo.update_row(new_data.model_dump(), item)
  return result


async def delete_purchase_services(repo: PurchasesRepository, uid: uuid.UUID) -> None:
  item = await get_one_purchase_services(repo,uid)
  await repo.delete_row(item)
  return None

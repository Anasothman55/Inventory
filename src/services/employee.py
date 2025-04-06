

from sqlalchemy.exc import IntegrityError

import uuid

from rich import print

from ..db.models import EmployeeModel
from ..utils.employee import EmployeeRepository
from ..schema.employee import BaseEmployeeSchema
from ..exceptions.employee import (
  EmployeeNotFound,
  EmployeeAlreadyExists
)



async def create_employee_services(
    user_uid:uuid.UUID,
    repo: EmployeeRepository,
    req_data:BaseEmployeeSchema) -> EmployeeModel:

  try:
    new_data = req_data.model_dump()
    new_data.update({"user_uid": user_uid})

    new_row = EmployeeModel(**new_data )
    result = await repo.create_row(new_row)
    return result
  except IntegrityError as e:
    raise EmployeeAlreadyExists(req_data.name)

async def get_one_employee_services(repo: EmployeeRepository, uid: uuid.UUID) -> EmployeeModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise EmployeeNotFound(uid)
  return result


async def update_employee_services(
    repo: EmployeeRepository,
    uid: uuid.UUID, req_data: BaseEmployeeSchema) -> EmployeeModel:
  emp = await get_one_employee_services(repo,uid)
  result = await repo.update_row(req_data.model_dump(), emp)
  return result


async def delete_employee_services(repo: EmployeeRepository, uid: uuid.UUID) -> None:
  emp = await get_one_employee_services(repo,uid)
  await repo.delete_row(emp)
  return None
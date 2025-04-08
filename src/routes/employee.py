import uuid
from typing import Annotated, List

from fastapi import APIRouter, status, Depends, Path, Query, Form


from ..db.models import UserModel, EmployeeModel
from ..dependencies.auth import require_roles, get_current_user
from ..schema.employee import BaseEmployeeSchema, Order, OrderBy,EmployeeWithInfoSchema, EmployeeFullSchema, EmployeeWithUseSchema
from ..schema.auth import RoleBase
from ..utils.employee import EmployeeRepository, get_employee_repo
from ..services.employee import (
  get_one_employee_services,
  create_employee_services,
  update_employee_services,
  delete_employee_services
)

from rich import print

alter_role = [RoleBase.ADMIN, RoleBase.ACCOUNTANT]
see_role = [RoleBase.ADMIN, RoleBase.ACCOUNTANT, RoleBase.MANAGER]

alter_role_des = f"""this route can use by all {RoleBase.ADMIN} and { RoleBase.ACCOUNTANT} users"""
see_role_des = f"""this route can use by all {RoleBase.ADMIN} and {RoleBase.ACCOUNTANT} and {RoleBase.MANAGER} users"""
admin_des = f"""this route can use by all {RoleBase.ADMIN} users"""


route = APIRouter(
  dependencies=[Depends(get_current_user)],
  tags=["Employees"]
)

@route.get('/', response_model= List[EmployeeWithUseSchema], status_code= status.HTTP_200_OK)
async def get_all_employee(
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
    order_by: Annotated[OrderBy, Query()] = OrderBy.CREATED_AT,
    order: Annotated[Order, Query()] = Order.ASC,
):
  f"""this route can use by all users"""
  res = await repo.get_all(order,order_by)
  return res


@route.post("/",response_model=BaseEmployeeSchema, status_code=status.HTTP_201_CREATED, description=alter_role_des)
async def create_category(
    req_data: Annotated[BaseEmployeeSchema, Form()],
    current_user: Annotated[UserModel, Depends(require_roles(alter_role))],
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
):
  result = await create_employee_services(current_user.uid,repo,req_data)
  return result


@route.get('/{uid}',  status_code= status.HTTP_200_OK, response_model=EmployeeWithUseSchema)
async def get_one_categories(
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
    uid: Annotated[uuid.UUID, Path(...)]
):
  result = await get_one_employee_services(repo,uid)
  return result


@route.patch("/{uid}", status_code=status.HTTP_200_OK, description=admin_des )
async def update_category(
    current_user: Annotated[UserModel, Depends(require_roles([RoleBase.ADMIN]))],
    uid: Annotated[uuid.UUID,Path(...)],
    new_data: Annotated[BaseEmployeeSchema, Form()],
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
):
  result = await update_employee_services(repo, uid, new_data)
  return result

@route.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT, description=admin_des)
async def delete_category(
    current_user: Annotated[UserModel, Depends(require_roles([RoleBase.ADMIN]))],
    uid: Annotated[uuid.UUID, Path(...)],
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
):
  await delete_employee_services(repo, uid)




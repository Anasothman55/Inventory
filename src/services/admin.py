from ..schema.auth import UpdateUserSchema, RoleBase
from ..utils.auth import UserRepositoryUtils,hash_password_utils
from ..db.models import UserModel
from ..exceptions.auth import UserNotFoundError, DeleteAdminError, AlterAdminError

import uuid



async def get_one_user_services(repo: UserRepositoryUtils, uid: uuid.UUID) -> UserModel:
  result = await repo.get_by_uid(uid)
  if not result:
    raise UserNotFoundError(uid)
  return result


async def update_user_services(
    repo: UserRepositoryUtils,
    uid: uuid.UUID,
    new_data: UpdateUserSchema) -> UserModel:
  user = await get_one_user_services(repo,uid)
  if user.role == RoleBase.ADMIN:
    raise AlterAdminError
  user_data = new_data.model_dump()
  if user_data.get("password"):
    hashing = hash_password_utils(user_data.get("password"))
    user_data['password'] = hashing
  result = await repo.update_row(user_data, user)
  return result



async def delete_user_services(repo: UserRepositoryUtils, uid: uuid.UUID) -> None:
  user = await get_one_user_services(repo,uid)
  if user.role == RoleBase.ADMIN:
    raise DeleteAdminError
  await repo.delete_row(user)
  return None









from fastapi import HTTPException, status


class EmployeeExceptions(HTTPException):
  pass

class EmployeeNotFound(EmployeeExceptions):
  def __init__(self, uid):
    message = "Employee not found" if uid is None else f"Employee with id {uid} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )


class EmployeeAlreadyExists(EmployeeExceptions):
  def __init__(self, name):
    message = f"Employee with name {name} already exists"
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

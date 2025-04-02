from fastapi import HTTPException, status


class PurchaseExceptions(HTTPException):
  pass

class PurchaseNotFound(PurchaseExceptions):
  def __init__(self, id):
    message = "Purchase not found" if id is None else f"Purchase with id {id} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )


class PurchaseAlreadyExists(PurchaseExceptions):
  def __init__(self, name, number):
    message = f"Purchase with purchase please {name} and receipt number {number} already exists"
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

from fastapi import HTTPException, status


class PurchaseItemsExceptions(HTTPException):
  pass

class PurchaseItemsNotFound(PurchaseItemsExceptions):
  def __init__(self, uid):
    message = "Purchase not found" if uid is None else f"Purchase with id {uid} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )

class PurchaseItemsMissingPart(PurchaseItemsExceptions):
  def __init__(self, field):
    super().__init__(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail= {
        "error": f"Missing required field: {field}",
      }
    )

class PurchaseItemsAlreadyExists(PurchaseItemsExceptions):
  def __init__(self):
    message = f""
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

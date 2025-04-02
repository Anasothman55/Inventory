from fastapi import HTTPException, status


class ItemsExceptions(HTTPException):
  pass

class ItemsNotFound(ItemsExceptions):
  def __init__(self, item_id):
    message = "Items not found" if item_id is None else f"Item with id {item_id} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )


class ItemsAlreadyExists(ItemsExceptions):
  def __init__(self, item_name):
    message = f"Item with name {item_name} already exists"
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

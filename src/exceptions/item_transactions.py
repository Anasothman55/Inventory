from fastapi import HTTPException, status


class TransactionsExceptions(HTTPException):
  pass

class TransactionsNotFound(TransactionsExceptions):
  def __init__(self, uid):
    message = "Transactions not found" if uid is None else f"Transactions with id {uid} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )


class TransactionsStock(TransactionsExceptions):
  def __init__(self):
    message = f"The use item are more than the stock"
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

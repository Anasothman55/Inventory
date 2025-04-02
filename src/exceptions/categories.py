from fastapi import HTTPException, status


class CategoriesExceptions(HTTPException):
  pass

class CategoriesNotFound(CategoriesExceptions):
  def __init__(self, categories_id):
    message = "Categories not found" if categories_id is None else f"Category with id {categories_id} not found"
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= {
        "error": message,
      }
    )


class CategoriesAlreadyExists(CategoriesExceptions):
  def __init__(self, categories_name):
    message = f"Category with name {categories_name} already exists"
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "error": message,
      }
    )

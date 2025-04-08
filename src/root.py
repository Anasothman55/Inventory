from fastapi import  APIRouter, Depends, Response, status, HTTPException,Request
from typing import Annotated
from sqlalchemy import  text
from sqlalchemy.ext.asyncio import AsyncSession


from .db.index import get_db
from .rate_limiter import limiter

from rich import print

roots = APIRouter()




@roots.get("/helth", status_code=status.HTTP_200_OK)
async def helth(db: Annotated[AsyncSession, Depends(get_db)]):
  try:
    result = await db.execute(text("SELECT 1"))
    await db.commit()

    return {
      "status": "healthy",
      "database": "connected",
      "message": "Application is running normally",
      "execute": result
    }
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail=f"Database connection failed: {str(e)}"
    )



@roots.get("/")
@limiter.limit("10/minute", error_message="you rich your limit")
async def root_route(request: Request):
  return {"message": "Welcome to FastAPI Project"}


from .routes.admin import route as admin_route
from .routes.auth import route as auth_route
from .routes.items import route as items_route
from .routes.categories import route as categories_route
from .routes.purchase import route as purchase_route
from .routes.purchase_items import route as purchase_items_route
from .routes.employee import route as employee_route
from .routes.item_transactions import route as item_transaction_route

roots.include_router(admin_route,prefix='/0a6c5da9793b254a/d658ddbfe93013bf/admin')
roots.include_router(auth_route,prefix="/auth")
roots.include_router(categories_route, prefix="/categories")
roots.include_router(items_route, prefix="/items")
roots.include_router(employee_route, prefix="/employees")
roots.include_router(purchase_route, prefix="/purchases")
roots.include_router(purchase_items_route, prefix="/purchase-items")
roots.include_router(item_transaction_route, prefix="/transactions")
from fastapi import  APIRouter, Depends, Response, status, HTTPException,Request
from typing import Annotated
from sqlalchemy import  text
from sqlalchemy.ext.asyncio import AsyncSession


from .db.index import get_db

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
async def root_route(request: Request):
  return {"message": "Welcome to FastAPI Project"}



from .routes.auth import route as auth_route
from .routes.items import route as items_route
from .routes.categories import route as categories_route

roots.include_router(auth_route,prefix="/auth")
roots.include_router(categories_route, prefix="/categories")
roots.include_router(items_route, prefix="/items")


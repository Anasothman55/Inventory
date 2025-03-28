from rich import  print

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  HTTPException, Response,Request


class RefreshTokenMiddleware(BaseHTTPMiddleware):
  async def dispatch(self,request: Request, call_next):
    response = await call_next(request)
    return response



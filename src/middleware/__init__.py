from fastapi import Request
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware
import logging



class CatchAllExceptionsMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    try:
      response = await call_next(request)
      return response
    except Exception as e:
      logging.error(f"Unhandled error: {e}", exc_info=True)
      return JSONResponse(
        status_code=500,
        content={"detail": {
          "error": "Something went wrong on our side. Please try again.",
          "server_error": str(e)
        }},
      )




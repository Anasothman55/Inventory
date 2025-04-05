from fastapi import APIRouter, status, Depends, Path, Request, responses, Query, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from ..dependencies.auth import require_roles
from ..schema.auth import RoleBase

from rich import print
from datetime import datetime, timezone
import orjson
import json


route = APIRouter(
  dependencies=[Depends(require_roles([RoleBase.ADMIN]))],
  tags=["Admin"]
)


@route.get('/')
async def read_admin_users() :
  pass











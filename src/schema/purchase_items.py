
from pydantic import BaseModel

from decimal import  Decimal


class BasePurchaseItemSchema(BaseModel):
  quantity: int
  unite_price: Decimal
  subtotal_price : Decimal
  note: str





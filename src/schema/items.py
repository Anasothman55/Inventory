from pydantic import  BaseModel




class ItemsBaseSchema(BaseModel):
  item_nameL : str
  stock : int
  unit : str
  minimum_stock_level : int





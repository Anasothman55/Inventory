

import uvicorn

if __name__ == "__main__":
  uvicorn.run("src.main:app", port=8002, reload=True)


"""
alembic
1- alembic init -t async migrations
2- alembic revision --autogenerate -m "3st migrations"
3- alembic upgrade b82f004289b0    
""" 


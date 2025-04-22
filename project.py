
from rich import print
import uvicorn

if __name__ == "__main__":
  uvicorn.run("src.main:app",host="0.0.0.0", port=8000,log_level="debug", reload=True)


"""
alembic
1- alembic init -t async migrations
2- alembic revision --autogenerate -m "3st migrations"
3- alembic upgrade 9252446b8f25    
""" 




import uvicorn

if __name__ == "__main__":
  uvicorn.run("src.main:app", port=8000, reload=True)


"""
alembic
1- alembic init -t async migrations
2- alembic revision --autogenerate -m "4st migrations"
3- alembic upgrade 2b6db675235f    
""" 




import uvicorn

if __name__ == "__main__":
  uvicorn.run("src.main:app", port=8002,log_level="debug", reload=True)


"""
alembic
1- alembic init -t async migrations
2- alembic revision --autogenerate -m "2st migrations"
3- alembic upgrade 0af107c949a8    
""" 


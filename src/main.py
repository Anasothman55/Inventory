from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from contextlib import  asynccontextmanager

from .root import roots
from .db.index import init_db, close_db_connection, get_db
from .logging import configure_logging, LogLevels
from .middleware import CatchAllExceptionsMiddleware

configure_logging(LogLevels.debug)

@asynccontextmanager
async def life_span(app: FastAPI):
  try:  
    await init_db()
  except Exception as e:
    print("Error during startup: " + str(e))
    raise
  yield
  try:
    await close_db_connection()
    print("Application shutdown complete")
  except Exception as e:
    print(f"Error closing database connection: {str(e)}")


app = FastAPI(title="FastAPI Project", version="0.1.0", lifespan=life_span)

origins = [
  "http://localhost:5173",  # React Frontend
  "http://127.0.0.1:5173",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,  # Allow specific frontend origins
  allow_credentials=True,
  allow_methods=["*"],  # Allow all HTTP methods
  allow_headers=["*"],  # Allow all headers
)


app.add_middleware(CatchAllExceptionsMiddleware)

app.include_router(roots)




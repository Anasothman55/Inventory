
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ..core.config import setting
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from sqlmodel import SQLModel,text
from ..utils.auth import UserRepositoryUtils, UserModel, hash_password_utils

from rich import print

engine = create_async_engine(
  url= setting.POSTGRESQL_URI,
  echo= False,
  
  pool_size=10,
  max_overflow=20,
  pool_timeout=30,
  pool_recycle=3600,
)



async_session_maker = sessionmaker(
  bind=engine,
  class_ = AsyncSession,
  expire_on_commit=False
)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    try:
      yield session
    except Exception as e:
      await session.rollback()
      raise
    finally:
      await session.close()

async def close_db_connection():
  await engine.dispose()


async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully")

  async with async_session_maker() as db:
    # Check if an admin user already exists
    user_repo = UserRepositoryUtils(db)
    result = await user_repo.get_by_role('admin')

    if not result:
      dumped = {
        'username': 'Admin',
        'email': 'anasothman581@gmail.com',
        'password': hash_password_utils('anasadmin'),
        'role': 'admin'
      }

      res = await user_repo.create(dumped)
      print(res)
    else:
      print("Admin user already exists")



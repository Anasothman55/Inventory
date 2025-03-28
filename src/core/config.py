
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  
  POSTGRESQL_URI: str
  SECRET_KEY: str
  ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_DAYS: int



model_config = SettingsConfigDict(
  env_file=".env",
  extra="ignore"
)

setting = Settings()

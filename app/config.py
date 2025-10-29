from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  APP_NAME: str = "Hello app"
  APP_ENV: str = "develop"
  DATABASE_URL: str = "sqlite:///./temp.db"

settings = Settings()
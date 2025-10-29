from fastapi import FastAPI
from app.config import settings
from app.routers import hello

app = FastAPI(
  title = settings.APP_NAME
)

if settings.APP_ENV == "develop":
  print('Running in "develop" mode. Using in-memory database.')
  # Set in-memory db

# Include routers
app.include_router(hello.router)

@app.get("/", tags=["Health Check"])
def health_check():
  return {"message": "I'm alive!"}
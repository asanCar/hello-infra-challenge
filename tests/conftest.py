import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers import hello

@pytest.fixture(scope="session") # Overwrite the default "function" scope 
def client() -> TestClient:
  """
  Create a TestClient to be used in tests
  """
  with TestClient(app) as client:
    yield client

@pytest.fixture(autouse=True)
def reset_database():
  """
  Fixture that automatically runs before every test
  to clear the in-memory database. This prevents
  data pollution between tests.
  """
  hello._db.clear()
  yield
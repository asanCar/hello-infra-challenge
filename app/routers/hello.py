from fastapi import APIRouter, HTTPException, status, Path
from app.models import UserBirthday
from datetime import date
from typing import Annotated

# Configure routes prefix and documentation group
router = APIRouter(
  prefix="/hello",
  tags=["Hello"]
)

# Simple implementation of an in-memory database
_db: dict[str, date] = {}

# Define a username Type with some validations
UsernameParam = Annotated[
  str,
  Path(
    ...,
    min_length=1,
    pattern=r"^[a-zA-Z]+$",
    title="Username"
  )
]

def _get_days_until_birthday(birthday: date) -> int:
  """
  Calculates the days until the next birthday.
  """
  today = date.today()

  # Retrieve birthday for the current year
  current_year_birthday = birthday.replace(year=today.year)

  # If birthday already passed this year
  if current_year_birthday < today:
    next_year_birthday = current_year_birthday.replace(year=today.year + 1)
    days_diff = (next_year_birthday - today).days
  else:
    days_diff = (current_year_birthday - today).days

  return days_diff

@router.get("/{username}")
def get_hello(username: UsernameParam):
  """
  Retrieves a greeting for a user.
  """
  if username not in _db:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User {username} not found"
    )

  birthday = _db[username]
  days_until = _get_days_until_birthday(birthday)

  if days_until == 0:
    message = f"Hello, {username}! Happy birthday!"
  else:
    message = f"Hello, {username}! Your birthday is in {days_until} day(s)"

  return {"message": message}

@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def put_hello(username: UsernameParam, birthday: UserBirthday):
  """
  Stores a user's birthday.
  """
  _db[username] = birthday.dateOfBirth
  return
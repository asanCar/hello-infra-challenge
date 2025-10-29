from pydantic import BaseModel, Field, field_validator
from datetime import date

class UserBirthday(BaseModel):
  """
  Model for the user's birthday payload.
  """
  dateOfBirth: date = Field(..., examples=["1990-10-30"]) # Use Elipsis to make it a mandatory field

  @field_validator("dateOfBirth")
  def date_of_birth_cannot_be_in_future(cls, v: date) -> date:
    """
    Validate that the date of birth is not a future date.
    """
    if v > date.today():
      raise ValueError("Date of birth cannot be in the future")
    return v
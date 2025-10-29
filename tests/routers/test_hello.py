from fastapi.testclient import TestClient
from datetime import date
from freezegun import freeze_time

def test_get_hello_user_not_found(client: TestClient):
  """
  Test that GET /hello/<username> returns 404
  if the user does not exist.
  """
  
  # Given
  username = "unknownuser"
  
  # When
  response = client.get(f"/hello/{username}")

  # Then
  ## Verify HTTP status code and body
  assert response.status_code == 404
  assert response.json() == {"detail": f"User {username} not found"}

def test_put_hello_user(client: TestClient):
  """
  Test that PUT /hello/<username> successfully stores
  a user's birthday.
  """
  
  # Given
  username = "testuser"
  today = date.today().isoformat()

  # When
  response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": today}
  )

  # Then
  ## Verify HTTP status code and that no bytes were sent at all
  assert response.status_code == 204
  assert response.content == b"" # More robust than just testing response.text

@freeze_time("2025-10-15")
def test_put_and_get_hello_user(client: TestClient):
  """
  Test that we can PUT a user's birthday and then
  GET the correct greeting message.
  """
  # Given
  username = "testuser"
  birthday = date(1999, 10, 25).isoformat()

  # When
  put_response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": birthday}
  )
  get_response = client.get(
    f"/hello/{username}"
  )

  # Then
  ## Verify HTTP status code from the PUT request
  assert put_response.status_code == 204

  ## Verify HTTP status code and body from the GET request
  assert get_response.status_code == 200
  assert get_response.json() == {
    "message": f"Hello, {username}! Your birthday is in 10 day(s)"
  }

@freeze_time("2025-10-29")
def test_get_hello_user_on_birthday(client: TestClient):
  """
  Test that GET /hello/<username> returns "Happy birthday!" message
  on the user's birthday.
  """
  # Given
  username = "testuser"
  birthday = date(1999, 10, 29).isoformat()

  # When
  put_response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": birthday}
  )
  get_response = client.get(
    f"/hello/{username}"
  )

  # Then
  ## Verify HTTP status code from the PUT request
  assert put_response.status_code == 204

  ## Verify HTTP status code and body from the GET request
  assert get_response.status_code == 200
  assert get_response.json() == {
    "message": f"Hello, {username}! Happy birthday!"
  }

@freeze_time("2025-10-29")
def test_get_hello_user_birthday_passed(client: TestClient):
  """
  Test that GET /hello/<username> correctly calculates the days
  until next year's birthday when the current's year birthday
  already passed.
  """
  # Given
  username = "testuser"
  birthday = date(1999, 10, 28).isoformat()

  # When
  put_response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": birthday}
  )
  get_response = client.get(
    f"/hello/{username}"
  )

  # Then
  ## Verify HTTP status code from the PUT request
  assert put_response.status_code == 204

  ## Verify HTTP status code and body from the GET request
  assert get_response.status_code == 200
  assert get_response.json() == {
    "message": f"Hello, {username}! Your birthday is in 364 day(s)"
  }

@freeze_time("2025-10-29")
def test_put_hello_user_future_birthday(client: TestClient):
  """
  Test that PUT /hello/<username> returns 422 error
  if the dateOfBirth is in the future.
  """
  # Given
  username = "testuser"
  birthday = date(2026, 1, 1).isoformat()

  # When
  response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": birthday}
  )

  # Then
  ## Verify HTTP status code
  assert response.status_code == 422

  ## Verify error message
  response_data = response.json()
  assert "detail" in response_data
  error_message = response_data["detail"][0]["msg"]
  assert "Date of birth cannot be in the future" in error_message

def test_put_hello_invalid_username(client: TestClient):
  """
  Test that PUT /hello/<username> returns 422 error
  if username contains non-letters.
  """
  # Given
  username = "testuser123"
  birthday = date.today().isoformat()

  # When
  response = client.put(
    f"/hello/{username}",
    json={"dateOfBirth": birthday}
  )

  # Then
  ## Verify HTTP status code
  assert response.status_code == 422

  ## Verify error the error is in the "username" path param
  response_data = response.json()
  assert "detail" in response_data
  error_message = response_data["detail"][0]["loc"] == ["path", "username"]

def test_get_hello_invalid_username(client: TestClient):
  """
  Test that GET /hello/<username> returns 422 error
  if username contains non-letters.
  """
  # Given
  username = "test-user"

  # When
  response = client.get(
    f"/hello/{username}"
  )

  # Then
  ## Verify HTTP status code
  assert response.status_code == 422

  ## Verify error the error is in the "username" path param
  response_data = response.json()
  assert "detail" in response_data
  error_message = response_data["detail"][0]["loc"] == ["path", "username"]
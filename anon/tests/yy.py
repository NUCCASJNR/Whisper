from django.core.asgi import get_asgi_application
from anon.api import MainUser
from httpx import AsyncClient
import pytest


@pytest.fixture
def create_existing_user():
    # Setup: Create and return an existing user
    user = MainUser(username="existing_user", password="password123", email="existinguser@example.com")
    user.save()
    yield user

    user.delete()

@pytest.mark.django_db
async def test_signup_username_exists(create_existing_user):
    # Use the fixture for an existing user
    payload = {
        "username": create_existing_user.username,
        "password": "password123",
        "email": "existinguser2@example.com"
    }

    # Use the appropriate app wrapper
    async with AsyncClient(app=get_asgi_application(), base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/auth/signup/", json=payload)

    # Assert that the response status is 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {
        "error": "Username already exists",
        "status": 400
    }

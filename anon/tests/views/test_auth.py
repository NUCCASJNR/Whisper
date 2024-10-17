import pytest
from rest_framework.test import APIRequestFactory
from anon.views.auth import SignUpViewSet
from anon.serializers.auth import SignUpSerializer
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "Testpassword0@",
    }


@pytest.fixture
def bad_data():
    return {
        "username": "",
        "password": "Testpassword@",
    }


@pytest.mark.django_db
def test_post_valid_data(request_factory, user_data, mocker):
    view = SignUpViewSet.as_view({"post": "create"})
    request = request_factory.post("/signup/", user_data, format="json")

    # Ensure the serializer validates the data correctly
    serializer = SignUpSerializer(data=user_data)
    assert serializer.is_valid()

    # Mock the generate_key_async function
    mocker.patch("anon.utils.task.generate_key_async", return_value="123456")

    # Get the response
    response = view(request)

    # Assertions for a successful signup
    assert response.data.get("status") == status.HTTP_201_CREATED
    assert response.data.get("message") == "Signup successful, You can now login"

    # Additional check to ensure the user is created
    user = User.objects.get(username=user_data["username"])
    assert user is not None


@pytest.mark.django_db
def test_post_invalid_data(request_factory, bad_data):
    view = SignUpViewSet.as_view({"post": "create"})
    request = request_factory.post("/signup/", bad_data, format="json")

    # Get the response
    response = view(request)

    # Assertions for a failed signup
    assert response.data.get("status") == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

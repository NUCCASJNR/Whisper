import pytest
from django.contrib.auth.hashers import check_password
from anon.models.user import MainUser


@pytest.mark.django_db
class TestMainUser:
    def test_create_user(self):
        user = MainUser.custom_save(
            **{"username": "testuser", "password": "testpassword123"}
        )
        assert user.username == "testuser"
        assert user.ready_to_chat is False

    def test_password_is_hashed(self):
        user = MainUser.objects.create_user(
            username="testuser", password="testpassword123"
        )
        assert not user.password == "testpassword123"
        assert check_password("testpassword123", user.password)

    def test_custom_save_method(self):
        user = MainUser.custom_save(username="testuser", password="testpassword123")
        retrieved_user = MainUser.objects.get(username="testuser")
        assert not retrieved_user.password == "testpassword123"
        assert check_password("testpassword123", retrieved_user.password)

    def test_ready_to_chat_default(self):
        user = MainUser.objects.create_user(
            username="testuser", password="testpassword123"
        )
        assert user.ready_to_chat is False

    def test_unique_username_constraint(self):
        MainUser.objects.create_user(username="testuser", password="testpassword123")
        with pytest.raises(Exception):
            MainUser.objects.create_user(
                username="testuser", password="testpassword456"
            )

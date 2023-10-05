import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def author() -> User:
    return User.objects.create_user("author", email="author")


@pytest.fixture
def admin_user() -> User:
    return User.objects.create_user("admin_user", email="admin_user", is_staff=True)


@pytest.fixture
def non_admin_user() -> User:
    return User.objects.create_user("non_admin_user", email="non_admin_user")


@pytest.fixture
def anonymous_user() -> User:
    return None


def create_object(model, resource_data):
    return model.objects.create(**resource_data)


def get_object_data(source_object, fields) -> dict:
    if isinstance(source_object, dict):
        return {field: source_object[field] for field in fields}
    return {field: getattr(source_object, field) for field in fields}

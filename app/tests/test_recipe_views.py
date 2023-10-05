import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cookbook.models import Cookbook
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def list_viewname() -> str:
    return "recipe-list"


@pytest.fixture
def detail_viewname() -> str:
    return "recipe-detail"


@pytest.fixture
def model():
    return Recipe


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
    return AnonymousUser()


@pytest.fixture
def cookbook(author):
    cookbook_data = {"title": "Test Cookbook", "author": author}
    return Cookbook.objects.create(**cookbook_data)


@pytest.fixture
def resource_data(author, cookbook) -> dict:
    return {
        "title": "Test title",
        "description": "Test description",
        "author": author,
        "cookbook": cookbook,
    }


@pytest.fixture
def created_object(model, resource_data):
    return model.objects.create(**resource_data)


def get_object_data(source_object, fields) -> dict:
    if isinstance(source_object, dict):
        return {field: source_object[field] for field in fields}
    return {field: getattr(source_object, field) for field in fields}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("anonymous_user", status.HTTP_200_OK),
    ],
)
def test_get_all_recipes(
    model, list_viewname, client, user, created_object, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(list_viewname))

    assert response.status_code == expected_status
    assert len(response.data) == 1
    assert response.data[0] == RecipeSerializer(created_object).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_201_CREATED),
        ("non_admin_user", status.HTTP_201_CREATED),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_create_recipe(
    model, list_viewname, client, resource_data, user, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.post(reverse(list_viewname), RecipeSerializer(resource_data).data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        assert model.objects.count() == 1
        created_object = model.objects.get()
        # The author of the recipe is the user creating it.
        fields = resource_data.keys() - {"author"}
        assert get_object_data(resource_data, fields) == get_object_data(
            created_object, fields
        )
        assert created_object.author == user_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("anonymous_user", status.HTTP_200_OK),
    ],
)
def test_get_recipe(
    model, detail_viewname, client, user, created_object, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(detail_viewname, args=[created_object.id]))

    assert response.status_code == expected_status
    assert response.data == RecipeSerializer(created_object).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("author", status.HTTP_200_OK),
        ("admin_user", status.HTTP_200_OK),
        ("non_admin_user", status.HTTP_403_FORBIDDEN),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_update_recipe(
    model, detail_viewname, client, user, created_object, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    updated_data = {"title": "Updated title"}
    response = client.patch(
        reverse(detail_viewname, args=[created_object.id]), updated_data
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert model.objects.count() == 1
        updated_object = model.objects.get()
        fields = updated_data.keys()
        assert get_object_data(updated_data, fields) == get_object_data(
            updated_object, fields
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("author", status.HTTP_204_NO_CONTENT),
        ("admin_user", status.HTTP_204_NO_CONTENT),
        ("non_admin_user", status.HTTP_403_FORBIDDEN),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_delete_recipe(
    model, detail_viewname, client, user, created_object, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.delete(reverse(detail_viewname, args=[created_object.id]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not model.objects.filter(id=created_object.id).exists()

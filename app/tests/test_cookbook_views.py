from django.urls import reverse
from rest_framework import status

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer
from fixtures import *


@pytest.fixture
def list_viewname() -> str:
    return "cookbook-list"


@pytest.fixture
def detail_viewname() -> str:
    return "cookbook-detail"


@pytest.fixture
def model():
    return Cookbook


@pytest.fixture
def resource_data(author) -> dict:
    return {
        "title": "Test title",
        "description": "Test description",
        "author": author,
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("anonymous_user", status.HTTP_200_OK),
    ],
)
def test_get_all_cookbooks(
    model, list_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_object(model, resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(list_viewname))

    assert response.status_code == expected_status
    assert len(response.data) == 1
    assert response.data[0] == CookbookSerializer(created_object).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_201_CREATED),
        ("non_admin_user", status.HTTP_201_CREATED),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_create_cookbook(
    model, list_viewname, client, resource_data, user, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.post(
        reverse(list_viewname), CookbookSerializer(resource_data).data
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        assert model.objects.count() == 1
        created_object = model.objects.get()
        # The author of the cookbook is the user creating it.
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
def test_get_cookbook(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_object(model, resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(detail_viewname, args=[created_object.id]))

    assert response.status_code == expected_status
    assert response.data == CookbookSerializer(created_object).data


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
def test_update_cookbook(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_object(model, resource_data)
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
def test_delete_cookbook(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_object(model, resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.delete(reverse(detail_viewname, args=[created_object.id]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not model.objects.filter(id=created_object.id).exists()

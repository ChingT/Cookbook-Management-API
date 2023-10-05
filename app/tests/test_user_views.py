from django.urls import reverse
from rest_framework import status

from fixtures import *
from user.serializers import UserSerializer

User = get_user_model()


@pytest.fixture
def list_viewname() -> str:
    return "user-list"


@pytest.fixture
def detail_viewname() -> str:
    return "user-detail"


@pytest.fixture
def model():
    return User


@pytest.fixture
def resource_data() -> dict:
    return {"username": "test", "email": "test@email.com", "password": "test"}


def create_user(resource_data):
    return User.objects.create_user(**resource_data)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("non_admin_user", status.HTTP_200_OK),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_get_all_users(
    model, list_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_user(resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(list_viewname))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert len(response.data) == 2
        assert response.data[0] == UserSerializer(created_object).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_201_CREATED),
        ("non_admin_user", status.HTTP_201_CREATED),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_create_user(
    model, list_viewname, client, resource_data, user, expected_status, request
):
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.post(reverse(list_viewname), resource_data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        assert model.objects.count() == 2
        created_object = model.objects.get(id=response.data["id"])
        fields = resource_data.keys()
        assert get_object_data(resource_data, fields) == get_object_data(
            created_object, fields
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("anonymous_user", status.HTTP_200_OK),
    ],
)
def test_get_user(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_user(resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.get(reverse(detail_viewname, args=[created_object.id]))

    assert response.status_code == expected_status
    assert response.data == UserSerializer(created_object).data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("non_admin_user", status.HTTP_403_FORBIDDEN),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_update_user(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_user(resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    updated_data = {"username": "updated-username"}
    response = client.patch(
        reverse(detail_viewname, args=[created_object.id]), updated_data
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert model.objects.count() == 2
        updated_object = model.objects.get(id=created_object.id)
        fields = updated_data.keys()
        assert get_object_data(updated_data, fields) == get_object_data(
            updated_object, fields
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user, expected_status",
    [
        ("admin_user", status.HTTP_204_NO_CONTENT),
        ("non_admin_user", status.HTTP_403_FORBIDDEN),
        ("anonymous_user", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_delete_user(
    model, detail_viewname, client, user, resource_data, expected_status, request
):
    created_object = create_user(resource_data)
    user_fixture = request.getfixturevalue(user)
    client.force_authenticate(user=user_fixture)
    response = client.delete(reverse(detail_viewname, args=[created_object.id]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not model.objects.filter(id=created_object.id).exists()

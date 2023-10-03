from django.urls import path

from user_profile.views import ListUsersAPIView

urlpatterns = [
    path("", ListUsersAPIView.as_view(), name="user_profile-list"),
]

from django.urls import path

from user.views import ListUsersAPIView

urlpatterns = [
    path("", ListUsersAPIView.as_view()),
]

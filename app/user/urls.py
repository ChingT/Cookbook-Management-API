from django.urls import path

from user.views import GetUpdateDeleteUserAPIView, ListCreateUserAPIView

urlpatterns = [
    path("", ListCreateUserAPIView.as_view(), name="user-list"),
    path("<int:pk>/", GetUpdateDeleteUserAPIView.as_view(), name="user-detail"),
]

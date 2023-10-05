from django.urls import path

from cookbook.views import (
    GetUpdateDeleteCookbookAPIView,
    ListCreateCookbookAPIView,
    ToggleFavouriteCookbookAPIView,
)

urlpatterns = [
    path("", ListCreateCookbookAPIView.as_view(), name="cookbook-list"),
    path("<int:pk>/", GetUpdateDeleteCookbookAPIView.as_view(), name="cookbook-detail"),
    path(
        "toggle-favourite/<int:id>/",
        ToggleFavouriteCookbookAPIView.as_view(),
        name="cookbook-toggle",
    ),
]

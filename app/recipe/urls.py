from django.urls import path

from recipe.views import (
    GetUpdateDeleteRecipeAPIView,
    ListCreateRecipeAPIView,
    ToggleFavouriteRecipeAPIView,
)

urlpatterns = [
    path("", ListCreateRecipeAPIView.as_view(), name="recipe-list"),
    path("<int:pk>/", GetUpdateDeleteRecipeAPIView.as_view(), name="recipe-detail"),
    path(
        "toggle-favourite/<int:id>/",
        ToggleFavouriteRecipeAPIView.as_view(),
        name="recipe-toggle",
    ),
]

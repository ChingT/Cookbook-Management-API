from django.urls import path

from ingredient.views import (
    GetUpdateDeleteIngredientAPIView,
    ListCreateIngredientAPIView,
)

urlpatterns = [
    path("", ListCreateIngredientAPIView.as_view(), name="ingredient-list"),
    path(
        "<int:pk>/",
        GetUpdateDeleteIngredientAPIView.as_view(),
        name="ingredient-detail",
    ),
]

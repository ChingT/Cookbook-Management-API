from django.urls import path

from ingredient.views import (
    GetUpdateDeleteIngredientAPIView,
    ListCreateIngredientAPIView,
)

urlpatterns = [
    path("", ListCreateIngredientAPIView.as_view()),
    path("<int:pk>/", GetUpdateDeleteIngredientAPIView.as_view()),
]

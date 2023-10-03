from django.urls import path

from recipe.views import GetUpdateDeleteRecipeAPIView, ListCreateRecipeAPIView

urlpatterns = [
    path("", ListCreateRecipeAPIView.as_view()),
    path("<int:pk>/", GetUpdateDeleteRecipeAPIView.as_view()),
]

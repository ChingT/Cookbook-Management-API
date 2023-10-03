from django.urls import path

from cookbook.views import GetUpdateDeleteCookbookAPIView, ListCreateCookbookAPIView

urlpatterns = [
    path("", ListCreateCookbookAPIView.as_view()),
    path("<int:pk>/", GetUpdateDeleteCookbookAPIView.as_view()),
]

from django.urls import path

from cookbook.views import GetUpdateDeleteCookbookAPIView, ListCreateCookbookAPIView

urlpatterns = [
    path("", ListCreateCookbookAPIView.as_view(), name="cookbook-list"),
    path("<int:pk>/", GetUpdateDeleteCookbookAPIView.as_view(), name="cookbook-detail"),
]

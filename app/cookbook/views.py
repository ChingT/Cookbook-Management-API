from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer


class ListCreateCookbookAPIView(ListCreateAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer


class GetUpdateDeleteCookbookAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer

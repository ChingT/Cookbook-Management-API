from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer
from user.permissions import IsAdmin, IsAuthor, ReadOnly


class ListCreateCookbookAPIView(ListCreateAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GetUpdateDeleteCookbookAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

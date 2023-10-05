from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer
from user.permissions import IsAdmin, IsAuthor, ReadOnly


class ListCreateCookbookAPIView(ListCreateAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # The author of the cookbook is the user creating it.
        serializer.save(author=self.request.user)


class GetUpdateDeleteCookbookAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

    def perform_update(self, serializer):
        # Cannot change the author
        serializer.save(author=serializer.instance.author)


class ToggleFavouriteCookbookAPIView(GenericAPIView):
    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        cookbook = self.get_object()
        user = self.request.user
        if user in cookbook.favorite_by.all():
            cookbook.favorite_by.remove(user)
        else:
            cookbook.favorite_by.add(user)
        return Response(self.get_serializer(cookbook).data)

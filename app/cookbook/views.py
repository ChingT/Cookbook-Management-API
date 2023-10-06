from django.db.models import Q
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
    """
    get:
    Returns all cookbooks if no search parameter is given.
    If a search parameter is given, it returns all cookbooks that contain it in the
    title or description.

    post:
    Creates a new cookbook and returns it.
    """

    serializer_class = CookbookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Cookbook.objects.all()
        if search_string := self.request.query_params.get("search"):
            queryset = queryset.filter(
                Q(title__icontains=search_string)
                | Q(description__icontains=search_string)
            )
        return queryset

    def perform_create(self, serializer):
        # The author of the cookbook is the user creating it.
        serializer.save(author=self.request.user)


class GetUpdateDeleteCookbookAPIView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a cookbook based on the given id.

    patch:
    Partially updates and returns a cookbook based on the given id.

    delete:
    Deletes a cookbook based on the given id and return no content status 204.
    """

    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

    def perform_update(self, serializer):
        # Cannot change the author
        serializer.save(author=serializer.instance.author)


class ToggleFavouriteCookbookAPIView(GenericAPIView):
    """
    patch:
    Toggle starring cookbook by the logged-in user.
    """

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

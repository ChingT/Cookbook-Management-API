from django.db.models import Q
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from user.permissions import IsAdmin, IsAuthor, ReadOnly


class ListCreateRecipeAPIView(ListCreateAPIView):
    """
    get:
    Returns all recipes if no search parameter is given.
    If a search parameter is given, it returns all recipes that contain it in the
    title or description.

    post:
    Creates a new recipe and returns it.
    """

    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if search_string := self.request.query_params.get("search"):
            queryset = queryset.filter(
                Q(title__icontains=search_string)
                | Q(description__icontains=search_string)
            )
        return queryset

    def perform_create(self, serializer):
        # The author of the recipe is the user creating it.
        serializer.save(author=self.request.user)


class GetUpdateDeleteRecipeAPIView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a recipe based on the given id.

    patch:
    Partially updates and returns a recipe based on the given id.

    delete:
    Deletes a recipe based on the given id and return no content status 204.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

    def perform_update(self, serializer):
        # Cannot change the author
        serializer.save(author=serializer.instance.author)


class ToggleFavouriteRecipeAPIView(GenericAPIView):
    """
    patch:
    Toggle starring recipe by the logged-in user.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = self.request.user
        if user in recipe.favorite_by.all():
            recipe.favorite_by.remove(user)
        else:
            recipe.favorite_by.add(user)
        return Response(self.get_serializer(recipe).data)

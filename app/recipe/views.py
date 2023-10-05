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
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # The author of the recipe is the user creating it.
        serializer.save(author=self.request.user)


class GetUpdateDeleteRecipeAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

    def perform_update(self, serializer):
        # Cannot change the author
        serializer.save(author=serializer.instance.author)


class ToggleFavouriteRecipeAPIView(GenericAPIView):
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

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from user.permissions import IsAdmin, IsAuthor, ReadOnly


class ListCreateRecipeAPIView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GetUpdateDeleteRecipeAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthor | IsAdmin | ReadOnly]

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class ListCreateRecipeAPIView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class GetUpdateDeleteRecipeAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

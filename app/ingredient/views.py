from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer


class ListCreateIngredientAPIView(ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class GetUpdateDeleteIngredientAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

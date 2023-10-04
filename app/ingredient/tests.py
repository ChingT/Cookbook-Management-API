from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ingredient.models import Ingredient


class IngredientTests(APITestCase):
    def setUp(self):
        self.ingredient_data = {"name": "Test Ingredient"}
        self.ingredient = Ingredient.objects.create(**self.ingredient_data)

    def test_get_all_ingredients(self):
        url = reverse("ingredient-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertEqual(Ingredient.objects.get().name, self.ingredient.name)

    def test_create_ingredient(self):
        url = reverse("ingredient-list")
        ingredient_data = {"name": "New Ingredient"}
        response = self.client.post(url, ingredient_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)
        created_ingredient = Ingredient.objects.get(id=response.data["id"])
        self.assertEqual(created_ingredient.name, ingredient_data["name"])

    def test_get_ingredient(self):
        url = reverse("ingredient-detail", args=[self.ingredient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ingredient.objects.get().name, self.ingredient.name)

    def test_update_ingredient(self):
        url = reverse("ingredient-detail", args=[self.ingredient.id])
        updated_data = {"name": "Updated Ingredient"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ingredient.objects.get().name, updated_data["name"])

    def test_delete_ingredient(self):
        url = reverse("ingredient-detail", args=[self.ingredient.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=self.ingredient.id).exists())

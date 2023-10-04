from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ingredient.models import Ingredient

User = get_user_model()


class IngredientTests(APITestCase):
    def setUp(self):
        author = User.objects.create_user("test_user", password="0000")
        ingredient_data = {"name": "Test Ingredient"}
        ingredient = Ingredient.objects.create(**ingredient_data)
        self.created_data = {"id": ingredient.id, "name": ingredient.name}

    def test_get_all_ingredients(self):
        url = reverse("ingredient-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], self.created_data)

    def test_create_ingredient(self):
        url = reverse("ingredient-list")
        ingredient_data = {"name": "New Ingredient"}
        response = self.client.post(url, ingredient_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)
        created_ingredient = Ingredient.objects.get(id=response.data["id"])
        created_ingredient_data = {"name": created_ingredient.name}
        self.assertEqual(created_ingredient_data, ingredient_data)

    def test_get_ingredient(self):
        url = reverse("ingredient-detail", args=[self.created_data["id"]])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.created_data)

    def test_update_ingredient(self):
        url = reverse("ingredient-detail", args=[self.created_data["id"]])
        updated_data = {"name": "Updated Ingredient"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ingredient.objects.count(), 1)
        updated_ingredient = Ingredient.objects.get(id=response.data["id"])
        self.assertEqual(updated_ingredient.name, updated_data["name"])

    def test_delete_ingredient(self):
        url = reverse("ingredient-detail", args=[self.created_data["id"]])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=self.created_data["id"]).exists())

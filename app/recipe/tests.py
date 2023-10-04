from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cookbook.models import Cookbook
from recipe.models import Recipe

User = get_user_model()


class RecipeTests(APITestCase):
    def setUp(self):
        author = User.objects.create_user("test_user", password="0000")
        cookbook_data = {"title": "Test Cookbook", "author": author}
        cookbook = Cookbook.objects.create(**cookbook_data)
        recipe_data = {
            "title": "Test Recipe",
            "description": "Test description",
            "difficulty": 1,
            "author": author,
            "cookbook": cookbook,
        }
        recipe = Recipe.objects.create(**recipe_data)
        self.created_data = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "difficulty": recipe.difficulty,
            "author": recipe.author.id,
            "cookbook": recipe.cookbook.id,
        }

    def test_get_all_recipes(self):
        url = reverse("recipe-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], self.created_data)

    def test_create_recipe(self):
        url = reverse("recipe-list")
        recipe_data = {
            "title": "New Recipe",
            "description": "New description",
            "difficulty": 2,
            "author": self.created_data["author"],
            "cookbook": self.created_data["cookbook"],
        }
        response = self.client.post(url, recipe_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        created_recipe = Recipe.objects.get(id=response.data["id"])
        created_recipe_data = {
            "title": created_recipe.title,
            "description": created_recipe.description,
            "difficulty": created_recipe.difficulty,
            "author": created_recipe.author.id,
            "cookbook": created_recipe.cookbook.id,
        }
        self.assertEqual(created_recipe_data, recipe_data)

    def test_get_recipe(self):
        url = reverse("recipe-detail", args=[self.created_data["id"]])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.created_data)

    def test_update_recipe(self):
        url = reverse("recipe-detail", args=[self.created_data["id"]])
        updated_data = {"title": "Updated Recipe"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.count(), 1)
        updated_recipe = Recipe.objects.get(id=response.data["id"])
        self.assertEqual(updated_recipe.title, updated_data["title"])

    def test_delete_recipe(self):
        url = reverse("recipe-detail", args=[self.created_data["id"]])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.created_data["id"]).exists())

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cookbook.models import Cookbook
from recipe.models import Recipe


class RecipeTests(APITestCase):
    def setUp(self):
        author = User.objects.create_user("test_user", password="0000")
        cookbook_data = {"title": "Test Cookbook", "author": author}
        cookbook = Cookbook.objects.create(**cookbook_data)
        self.recipe_data = {
            "title": "Test Recipe",
            "author": author,
            "cookbook": cookbook,
        }
        self.recipe = Recipe.objects.create(**self.recipe_data)

    def test_get_all_recipes(self):
        url = reverse("recipe-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, self.recipe.title)
        self.assertEqual(Recipe.objects.get().author, self.recipe.author)

    def test_create_recipe(self):
        url = reverse("recipe-list")
        recipe_data = {
            "title": "Test Recipe",
            "author": self.recipe_data["author"].id,
            "cookbook": self.recipe_data["cookbook"].id,
        }
        response = self.client.post(url, recipe_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        created_recipe = Recipe.objects.get(id=response.data["id"])
        self.assertEqual(created_recipe.title, recipe_data["title"])
        self.assertEqual(created_recipe.author.id, recipe_data["author"])

    def test_get_recipe(self):
        url = reverse("recipe-detail", args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get().title, self.recipe.title)
        self.assertEqual(Recipe.objects.get().author, self.recipe.author)

    def test_update_recipe(self):
        url = reverse("recipe-detail", args=[self.recipe.id])
        updated_data = {"title": "Updated Recipe"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get().title, updated_data["title"])
        self.assertEqual(Recipe.objects.get().author, self.recipe.author)

    def test_delete_recipe(self):
        url = reverse("recipe-detail", args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

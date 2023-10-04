from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cookbook.models import Cookbook

User = get_user_model()


class CookbookTests(APITestCase):
    def setUp(self):
        author = User.objects.create_user("test_user", password="0000")
        self.cookbook_data = {"title": "Test Cookbook", "author": author}
        self.cookbook = Cookbook.objects.create(**self.cookbook_data)

    def test_get_all_cookbooks(self):
        url = reverse("cookbook-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cookbook.objects.count(), 1)
        self.assertEqual(Cookbook.objects.get().title, self.cookbook.title)
        self.assertEqual(Cookbook.objects.get().author, self.cookbook.author)

    def test_create_cookbook(self):
        url = reverse("cookbook-list")
        cookbook_data = {
            "title": "Test Cookbook",
            "author": self.cookbook_data["author"].id,
        }
        response = self.client.post(url, cookbook_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cookbook.objects.count(), 2)
        created_cookbook = Cookbook.objects.get(id=response.data["id"])
        self.assertEqual(created_cookbook.title, cookbook_data["title"])
        self.assertEqual(created_cookbook.author.id, cookbook_data["author"])

    def test_get_cookbook(self):
        url = reverse("cookbook-detail", args=[self.cookbook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cookbook.objects.get().title, self.cookbook.title)
        self.assertEqual(Cookbook.objects.get().author, self.cookbook.author)

    def test_update_cookbook(self):
        url = reverse("cookbook-detail", args=[self.cookbook.id])
        updated_data = {"title": "Updated Cookbook"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cookbook.objects.get().title, updated_data["title"])
        self.assertEqual(Cookbook.objects.get().author, self.cookbook.author)

    def test_delete_cookbook(self):
        url = reverse("cookbook-detail", args=[self.cookbook.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cookbook.objects.filter(id=self.cookbook.id).exists())

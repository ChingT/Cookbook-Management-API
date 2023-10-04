from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cookbook.models import Cookbook

User = get_user_model()


class CookbookTests(APITestCase):
    def setUp(self):
        author = User.objects.create_user("test_user", password="0000")
        cookbook_data = {
            "title": "Test Cookbook",
            "description": "Test description",
            "author": author,
        }
        cookbook = Cookbook.objects.create(**cookbook_data)
        self.created_data = {
            "id": cookbook.id,
            "title": cookbook.title,
            "description": cookbook.description,
            "author": cookbook.author.id,
        }

    def test_get_all_cookbooks(self):
        url = reverse("cookbook-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], self.created_data)

    def test_create_cookbook(self):
        url = reverse("cookbook-list")
        cookbook_data = {
            "title": "New Cookbook",
            "description": "New description",
            "author": self.created_data["author"],
        }
        response = self.client.post(url, cookbook_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cookbook.objects.count(), 2)
        created_cookbook = Cookbook.objects.get(id=response.data["id"])
        created_cookbook_data = {
            "title": created_cookbook.title,
            "description": created_cookbook.description,
            "author": created_cookbook.author.id,
        }
        self.assertEqual(created_cookbook_data, cookbook_data)

    def test_get_cookbook(self):
        url = reverse("cookbook-detail", args=[self.created_data["id"]])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.created_data)

    def test_update_cookbook(self):
        url = reverse("cookbook-detail", args=[self.created_data["id"]])
        updated_data = {"title": "Updated Cookbook"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cookbook.objects.count(), 1)
        updated_cookbook = Cookbook.objects.get(id=response.data["id"])
        self.assertEqual(updated_cookbook.title, updated_data["title"])

    def test_delete_cookbook(self):
        url = reverse("cookbook-detail", args=[self.created_data["id"]])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cookbook.objects.filter(id=self.created_data["id"]).exists())

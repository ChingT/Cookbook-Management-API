from django.contrib.auth.models import User
from django.db import models


class Cookbook(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="cookbooks"
    )
    favourite_by_users = models.ManyToManyField(to=User, blank=True)

    def __str__(self):
        return f"Cookbook '{self.title}'"

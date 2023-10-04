from django.contrib.auth import get_user_model
from django.db import models

from cookbook.models import Cookbook
from ingredient.models import Ingredient

User = get_user_model()


class Recipe(models.Model):
    class Difficulty(models.IntegerChoices):
        Easy = 1
        Intermediate = 2
        Hard = 3

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(to=Ingredient)
    difficulty = models.IntegerField(choices=Difficulty.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cookbook = models.ForeignKey(
        to=Cookbook, on_delete=models.CASCADE, related_name="recipes"
    )
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="recipes"
    )

    def __str__(self):
        return f"Recipe '{self.title}'"

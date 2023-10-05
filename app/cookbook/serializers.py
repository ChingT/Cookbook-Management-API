from rest_framework import serializers

from cookbook.models import Cookbook
from recipe.serializers import RecipeSerializer
from user.serializers import UserSerializer


class CookbookSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    recipes = RecipeSerializer(many=True, read_only=True)
    favorite_by = UserSerializer(many=True, read_only=True)
    logged_in_user_favourite = serializers.SerializerMethodField()
    is_from_logged_in_user = serializers.SerializerMethodField()

    def get_logged_in_user_favourite(self, instance):
        user = self.context["request"].user
        return (
            user.is_authenticated and instance.favorite_by.filter(id=user.id).exists()
        )

    def get_is_from_logged_in_user(self, instance):
        user = self.context["request"].user
        return instance.author == user

    class Meta:
        model = Cookbook
        fields = [
            "id",
            "title",
            "description",
            "recipes",
            "author",
            "favorite_by",
            "logged_in_user_favourite",
            "is_from_logged_in_user",
        ]

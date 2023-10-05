from rest_framework import serializers

from recipe.models import Recipe
from user.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["author"] = UserSerializer(instance.author).data
        response["favorite_by"] = UserSerializer(instance.favorite_by, many=True).data
        return response

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "cookbook",
            "author",
            "favorite_by",
            "logged_in_user_favourite",
            "is_from_logged_in_user",
        ]
        read_only_fields = ["author", "recipes", "favorite_by"]

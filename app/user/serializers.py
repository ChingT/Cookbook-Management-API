from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    amount_of_favorite_cookbooks = serializers.SerializerMethodField()
    amount_of_favorite_recipes = serializers.SerializerMethodField()

    def get_amount_of_favorite_cookbooks(self, instance):
        return instance.favorite_cookbooks.count()

    def get_amount_of_favorite_recipes(self, instance):
        return instance.favorite_recipes.count()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "cookbooks",
            "recipes",
            "amount_of_favorite_cookbooks",
            "amount_of_favorite_recipes",
        ]
        read_only_fields = [
            "cookbooks",
            "recipes",
            "amount_of_favorite_cookbooks",
            "amount_of_favorite_recipes",
        ]

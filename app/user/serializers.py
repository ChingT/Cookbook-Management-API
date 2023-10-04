from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    amount_of_cookbooks = serializers.SerializerMethodField()
    amount_of_recipes = serializers.SerializerMethodField()

    def get_amount_of_cookbooks(self, instance):
        return instance.cookbooks.all().count()

    def get_amount_of_recipes(self, instance):
        return instance.recipes.all().count()

    class Meta:
        model = User
        fields = ["id", "username", "amount_of_cookbooks", "amount_of_recipes"]

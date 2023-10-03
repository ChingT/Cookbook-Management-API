from rest_framework import serializers

from cookbook.models import Cookbook


class CookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookbook
        fields = ["id", "title", "description", "author"]

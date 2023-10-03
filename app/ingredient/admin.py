from django.contrib import admin

from ingredient.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ["name"]

    def get_list_display(self, request):
        return [field.name for field in Ingredient._meta.fields]

    def get_search_fields(self, request):
        return [field.name for field in Ingredient._meta.fields]


admin.site.register(Ingredient, IngredientAdmin)

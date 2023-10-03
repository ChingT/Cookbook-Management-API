from django.contrib import admin

from recipe.models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ["ingredients", "difficulty"]

    def get_list_display(self, request):
        return [field.name for field in Recipe._meta.fields]

    def get_search_fields(self, request):
        return [field.name for field in Recipe._meta.fields]


admin.site.register(Recipe, RecipeAdmin)

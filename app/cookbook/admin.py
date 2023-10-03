from django.contrib import admin

from cookbook.models import Cookbook


class CookbookAdmin(admin.ModelAdmin):
    list_filter = ["author"]

    def get_list_display(self, request):
        return [field.name for field in Cookbook._meta.fields]

    def get_search_fields(self, request):
        return [field.name for field in Cookbook._meta.fields]


admin.site.register(Cookbook, CookbookAdmin)

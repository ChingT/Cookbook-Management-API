"""
URL configuration for cookbook_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Cookbook management API",
        default_version="v1",
        description="A Recipe and Cookbook Management API, which allows you to manage "
        "recipes, cookbooks, ingredients and users.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Set to False restrict access to protected endpoints
    permission_classes=[permissions.AllowAny],  # Permissions for docs access
)


auth_urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]

api_urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    path("cookbooks/", include("cookbook.urls")),
    path("ingredients/", include("ingredient.urls")),
    path("recipes/", include("recipe.urls")),
    path("auth/", include(auth_urlpatterns)),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = [path("api/", include(api_urlpatterns))]

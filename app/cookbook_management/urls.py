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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class AuthViews:
    """Class to encapsulate authentication-related views."""

    @classmethod
    def as_view(cls):
        return [
            path("", TokenObtainPairView.as_view(), name="token_obtain"),
            path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
            path("verify/", TokenVerifyView.as_view(), name="token_verify"),
        ]


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/users/", include("user.urls")),
    path("api/cookbooks/", include("cookbook.urls")),
    path("api/ingredients/", include("ingredient.urls")),
    path("api/recipes/", include("recipe.urls")),
    path("api/auth/", include(AuthViews.as_view())),
]

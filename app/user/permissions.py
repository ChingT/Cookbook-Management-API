from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

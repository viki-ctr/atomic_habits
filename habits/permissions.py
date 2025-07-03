from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешение только для владельца привычки"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicReadOnly(permissions.BasePermission):
    """Разрешение только для чтения публичных привычек"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.is_public

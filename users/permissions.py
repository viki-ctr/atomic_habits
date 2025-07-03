from rest_framework import permissions


class IsSelfOrReadOnly(permissions.BasePermission):
    """Разрешает редактирование только своего профиля"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

from rest_framework import permissions


class AuthorAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ModeratorAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
        )


class AdminAccess(permissions.BasePermission):
    def has_permission(self, request, view,):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только для администратора.
    """
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff

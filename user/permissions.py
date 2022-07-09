from rest_framework import permissions

class IsUserOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsSuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_superuser)
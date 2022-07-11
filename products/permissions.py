from rest_framework import permissions

class IsSellerOrGetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            if not request.user.is_seller:
                return False
        except:
            return False

        return (request.user.is_authenticated)

class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.seller == request.user
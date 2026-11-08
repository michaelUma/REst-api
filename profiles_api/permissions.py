from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Require authentication and restrict profile changes to the profile owner."""

    def has_permission(self, request, view):
        """Only authenticated users may access profile endpoints."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Allow safe reads; only the owner may modify a profile."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Require authentication and restrict access to the profile owner."""

    def has_permission(self, request, view):
        """Only authenticated users may access profile endpoints."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Allow users to access only their own profile object."""
        return obj.pk == request.user.pk

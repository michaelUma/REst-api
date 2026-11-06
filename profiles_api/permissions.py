from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow public registration and restrict profile access to its owner."""

    def has_permission(self, request, view):
        # Registration is intentionally public. All other profile actions
        # require an authenticated user.
        if getattr(view, "action", None) == "create":
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Allow an authenticated user to access only their own profile."""

        return bool(
            request.user
            and request.user.is_authenticated
            and obj.pk == request.user.pk
        )

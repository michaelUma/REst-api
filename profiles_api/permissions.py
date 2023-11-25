from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allows users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is to trying to edit their own profile"""

        #check if method is get i.e user only want to view
        if request.method in permissions.SAFE_METHODS:
            return True

        #if method is not get then will check if user wants to edit own profile
        return obj.id == request.user.ids
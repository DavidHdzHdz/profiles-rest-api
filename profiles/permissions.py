from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile """

    def has_object_permission(self, request, view, object):
        """ check if user is trying to edit his own profile """
        if request.method in permissions.SAFE_METHODS:
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            return True

        return object.id == request.user.id

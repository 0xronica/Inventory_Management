from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrWorker(BasePermission):
    """
    Owners: full access
    Workers: read + update quantity only
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'owner':
            return True

        if request.user.role == 'worker':
            if request.method in SAFE_METHODS:
                return True
            return request.method in ['PUT', 'PATCH']

        return False


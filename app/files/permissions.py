from rest_framework import permissions


class IsOwnerOrShared(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        if request.user in obj.shared_with.all():
            return True
        return False


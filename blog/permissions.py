from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'not authorized'

    def has_object_permission(self, request, view, obj):
        my_methods = ['GET']

        if request.method in my_methods:
            return True
            
        return obj.author == request.user


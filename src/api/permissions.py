from rest_framework.permissions import BasePermission, SAFE_METHODS
from notes.models import Note


class IsAuthorOrReadOnly(BasePermission):


    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return bool(request.user and request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # # мой вариант
        # if any((self.has_permission(request=request, view=view),
        #         request.method in SAFE_METHODS)):
        #     return True

        # не мой вариант
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.author




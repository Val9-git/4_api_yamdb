from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

'''
class IsModerator(BasePermission):
    """Позволять доступ только модераторам."""
'''


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(BasePermission):
    """Позволять доступ только админам."""
    message = 'Необходимы права администратора.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


'''
    
class IsAdmin(permissions.BasePermission):
    
    message = 'Необходимы права администратора.'
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)



class IsAuthor(BasePermission):
    """Позволять доступ только авторам."""
'''


class ReadOnly(BasePermission):
    """Позволять доступ только для чтения."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))

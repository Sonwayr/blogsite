from rest_framework import permissions


class CanRedactThemeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.has_perm('blog.change_theme'))


class CanRedactPostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user)
        return bool(request.user and (request.user.has_perm('blog.change_post')
                                      or request.user == obj.author))

from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrReadOnly(BasePermission):
    """
    Пермишен разрешает использовать безопасные запросы для всех пользователей
    и все остальные запросы только если пользователь является автором.
    """
    def has_permission(self, request, view):
        """
        Даст разрешение для безопасных запросов или для
        авторизированого пользователя.
        """
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Даст разрешение для безопасных запросов или
        если пользователь является автором.
        """
        return request.method in SAFE_METHODS or obj.author == request.user

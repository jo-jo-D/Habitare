from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Кастомное разрешение, которое позволяет редактировать объект
    только его владельцу. Остальным доступно только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_host


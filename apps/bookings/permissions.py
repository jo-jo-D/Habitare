from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Кастомное разрешение, которое позволяет редактировать объект
    только его владельцу. Остальным доступно только чтение.
    """
    def has_object_permission(self, request, view, obj):
        if request.method is 'POST':
            return request.user.can_host
        else:   #only owner can update delete or get all info
            return obj.booked_property.owner == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_host


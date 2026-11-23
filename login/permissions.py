from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permiso personalizado:
    - Un administrador (is_staff) tiene acceso total a cualquier usuario.
    - Un usuario regular (no admin) solo puede ver y editar SU PROPIO usuario.
    """
    def has_object_permission(self, request, view, obj):
        # Si es superadmin/staff, tiene permiso sobre cualquier registro
        if request.user and request.user.is_staff:
            return True

        # Para un usuario normal, permitimos si el objeto evaluado es él mismo
        return obj == request.user
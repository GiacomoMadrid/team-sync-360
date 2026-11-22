from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, status
from .serializers import UsuarioSerializer, PaisSerializer, GroupSerializer, TipoDocumentoSerializer, RegisterSerializer, ActivationSerializer, UsuarioAdminSerializer, UsuarioPerfilSelfSerializer, LogoutSerializer
from .models import Usuario, Group
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrSelf
from rest_framework.exceptions import NotFound
  

class UsuarioViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    ordering = ['apellido_p']

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        
        # Si es Administrador, usa el serializador completo
        if self.request.user and self.request.user.is_staff:
            return UsuarioAdminSerializer
            
        # Si es un usuario normal editando su propio perfil, usa el restringido
        return UsuarioPerfilSelfSerializer

    def get_queryset(self):
        user = self.request.user
        # Si el usuario no está autenticado, retornamos un queryset vacío
        if not user.is_authenticated:
            return Usuario.objects.none()
        
        # Si es administrador, ve a todos los usuarios
        if user.is_staff:
            return Usuario.objects.all()
        
        # Si es un usuario normal, solo se devuelve a sí mismo en los listados
        return Usuario.objects.filter(pk=user.pk)

    # CRUD
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.delete()
        return Response(
            {"message": "El usuario ha sido eliminado permanentemente."},
            status=status.HTTP_200_OK
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = '__all__'

    # De momento, los usuarios con el permiso de CRUD de Groups pueden hacer modificaciones sobre este.
    # Si lo que se requiere es que solo el admin pueda tener estos permisos, quitar el código de get_permissions y cambiar por:
    # permission_classes = [permissions.IsAdminUser]
    def get_permissions(self): 
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # ordering = ['id']


class UserRolesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            raise NotFound("Usuario no encontrado.")

    def get(self, request, user_id):
        user = self.get_user(user_id)
        roles = user.groups.values('id', 'name')
        return Response(list(roles))

    def post(self, request, user_id):
        user = self.get_user(user_id)
        role_ids = request.data.get('roles', [])
        roles = Group.objects.filter(id__in=role_ids)

        if roles.count() != len(set(role_ids)):
            return Response(
                {"detail": "Uno o más roles no existen."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.groups.add(*roles)

        return Response({
            "message": "Roles asignados correctamente."
        })

    def put(self, request, user_id):
        user = self.get_user(user_id)
        role_ids = request.data.get('roles', [])
        roles = Group.objects.filter(id__in=role_ids)

        if roles.count() != len(set(role_ids)):
            return Response(
                {"detail": "Uno o más roles no existen."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.groups.set(roles)

        return Response({
            "message": "Roles actualizados correctamente."
        })

    def delete(self, request, user_id, role_id):
        user = self.get_user(user_id)

        try:
            role = Group.objects.get(pk=role_id)
        except Group.DoesNotExist:
            raise NotFound("Rol no encontrado.")

        user.groups.remove(role)

        return Response({
            "message": "Rol revocado correctamente."
        })

from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Usuario
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


# Serializador para el ADMIN (Acceso total)
class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

# Serializador para el USUARIO NORMAL (Solo lectura en campos sensibles)
class UsuarioPerfilSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        # Definimos explícitamente todos los campos sensibles como solo lectura
        read_only_fields = [
            'id', 
            'email', 
            'password', 
            'usuario_administrador', 
            'usuario_activo', 
            'fecha_registro', 
            'last_login',
            'groups',             # Evita que cambie sus grupos
            'user_permissions'    # Evita que cambie sus permisos individuales
        ]



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            "email",
            "nombres",
            "apellido_p",
            "apellido_m"
        )

    def create(self, validated_data):
        user = Usuario(
            email=validated_data["email"],
            nombres=validated_data["nombres"],
            apellido_p=validated_data["apellido_p"],
            apellido_m=validated_data["apellido_m"],
            usuario_activo=True,
        )

        user.set_unusable_password()
        user.save()

        return user
    

class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate(self, data):
        try:
            uid = force_str(
                urlsafe_base64_decode(data["uid"])
            )

            user = Usuario.objects.get(pk=uid)

        except (
            TypeError,
            ValueError,
            OverflowError,
            Usuario.DoesNotExist
        ):
            raise serializers.ValidationError({
                "uid": "UID inválido."
            })

        if user.usuario_activo:
            raise serializers.ValidationError({
                "detail": "La cuenta ya se encuentra activada."
            })

        if not default_token_generator.check_token(
            user,
            data["token"]
        ):
            raise serializers.ValidationError({
                "token": "Token inválido o expirado."
            })

        self.user = user

        return data

    def save(self):
        user = self.user
        user.set_password(
            self.validated_data["new_password"]
        )

        user.usuario_activo = True
        user.save()

        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        try:
            token = RefreshToken(
                self.validated_data['refresh']
            )

            token.blacklist()

        except TokenError:
            raise serializers.ValidationError({
                "refresh": "Token inválido o ya expirado."
            })
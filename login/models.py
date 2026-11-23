from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from teamsync.settings import SECRET_KEY as sec_key 
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class UsuarioManager(BaseUserManager):
    def create_user(self, nombres, apellido_p, apellido_m, email, password):
        if not email:
            raise ValueError("El usuario debe registrar un correo electrónico")
        
        user = self.model(
            nombres = nombres,
            apellido_p = apellido_p, 
            apellido_m = apellido_m, 
            email = self.normalize_email(email),
            password = make_password(password, salt=None, hasher='default')
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nombres, apellido_p, apellido_m, email, password):
        user = self.create_user(
            nombres = nombres,
            apellido_p = apellido_p, 
            apellido_m = apellido_m, 
            email=email,
            password = password
        )
        user.usuario_administrador = True
        user.usuario_activo = True
        user.is_superuser = True
        user.save()
        return user



class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Correo electrónico", max_length = 255, unique = True)
    nombres = models.CharField("Nombres", max_length = 200, blank=False, null=False)
    apellido_p = models.CharField("Apellido paterno", max_length = 200, blank = True, null = False)
    apellido_m = models.CharField("Apellido materno", max_length = 200, blank = True, null = True)
    numero_celular = models.CharField("Celular", max_length = 20, blank = True, null = True)    
    usuario_administrador = models.BooleanField(default=False)
    usuario_activo = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha de Registro")

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombres", "apellido_p", "apellido_m"]
    
    def __str__(self):
        if(self.apellido_m == None):
            return f"{self.nombres} {self.apellido_p}"
                    
        return f"{self.nombres} {self.apellido_p} {self.apellido_m}"

    @property
    def is_staff(self):
        return self.usuario_administrador
    
    @property
    def is_active(self):
        return self.usuario_activo

    @property
    def date_joined(self):
        return self.fecha_registro

    def save(self, *args, **kwargs): # Hasheo de 
        is_new = self._state.adding        
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):     
            self.password = make_password(self.password)            
        super().save(*args, **kwargs)
        
        

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"



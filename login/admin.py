from django.contrib import admin
from .models import Usuario
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class UsuarioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Credenciales de acceso', {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombres', 'apellido_p', 'apellido_m', 'numero_celular')}),
        ('Permisos y Grupos', {'fields': ('usuario_activo', 'usuario_administrador', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_registro')}),
    )
    readonly_fields = ('fecha_registro', 'last_login')
    
    # Campos al crear un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombres', 'apellido_p', 'apellido_p', 'password1', 'password2'),
        }),
    )

    list_display = ('apellido_p', 'apellido_m',  'nombres', 'email', 'usuario_administrador', 'usuario_activo')
    search_fields = ('email', 'nombres', 'apellido_p', 'apellido_m')  
    
    ordering = ('apellido_p',)
    filter_horizontal = ('groups', 'user_permissions')

 

class SuperuserOnlyAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


for model in (OutstandingToken, BlacklistedToken):
    if admin.site.is_registered(model):
        admin.site.unregister(model)   


admin.site.register(Usuario, UsuarioAdmin)
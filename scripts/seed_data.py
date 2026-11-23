import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamsync.settings')
django.setup()

from login.models import Usuario, UsuarioManager
from django.contrib.admin.models import LogEntry

#Limpiar Data
LogEntry.objects.all().delete()
Usuario.objects.all().delete()

if not Usuario.objects.filter(email="admin@admin.com").exists():
    user = Usuario.objects.create_superuser(
        nombres="Admin",
        apellido_p="Superadmin",
        apellido_m="Superadmin",
        email="admin@admin.com",
        password="1234"
    )

    print("---------------------------------------")
    print("Super usuario creado: ID = ", user.id)
    print("Credenciales:")
    print("Correo: = ", user.email)
    print("Contraseña: = 1234")
    print("---------------------------------------")

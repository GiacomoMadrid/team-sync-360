import os
import sys
import django
from django.db import connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamsync.settings')
django.setup()

# IMPORTANTE: Este script no solo elimina la base de datos, sino que elimina todo el esquema completo. Luego de ejecutarlo tendrá que volver a ejecutar las migraciones y/o crear el esquema completo nuevamente

with connection.cursor() as cursor:
    cursor.execute("""
        DO
        $$
        DECLARE
            rec RECORD;
        BEGIN
            -- Eliminar todas las tablas del esquema 'public'
            FOR rec IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS "' || rec.tablename || '" CASCADE;';
            END LOOP;
        END
        $$;
    """)
    print("Todas las tablas fueron eliminadas correctamente.")
### (Re)Construir e iniciar contenedores

Si es la primera vez que se ejecuta o desea reconstruir el contenedor tras cambios en alguno de los archivos de configuración de Docker, ejecute el comando:

`docker compose build`

### Iniciar contenedores

Si, en cambio, el contenedor ya ha sido creado y tiene Docker desktop abierto, ejecute el siguiente comando en una terminal desde la raíz del proyecto

`docker compose up -d`

Esto le permitirá levantar el contenedor sin tener que reconstruirlo

### Ejecutar migraciones

Para generar las migraciones utilice:

`docker compose exec web python manage.py makemigrations`

Para ejecutar las migraciones utilice:

`docker compose exec web python manage.py migrate`


### Crear data inicial
Ejecutaremos el script de seed para la creación de la data inicial y el superusuario:

`docker compose exec web python scripts/seed_data.py`

### Detener

Para detener el servicio usaremos:

`docker compose down`

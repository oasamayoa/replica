# **Descripción**
Consiste en tener una base de datos por default como Postres, replica Mysql,
al momento de realizar un CRUD se vea cambios en ambos motores de BD del Modelo User.

### Lenguaje 
Python 3.11

### Frameworck
Django 4.2

### BD
Postgresql
Mysql

### Instalación de Entorno virtual
Crear un directorio de trabajo 
Dentro ejecutar
python -m venv nombre ejemplo python -m venv proyecto_env

**Activar entor virutal**
Entras a la carpeta 
cd proyecto_env/
cd Scripts/ 
activate

### Clonar proyecto
Dentro del directorio de Trabajo
ejectuar git clone url_del_proyecto

Entras al proyecto con el entorno activo
Ejecutar pip install -r requeriments.txt

### Ejectura migraciones a la base de datos
Siempre se trabaja dentro del proyecto ejecutar por pasos 
python manage.py makemigrations 
python manage.py migrate --database=default
python manage.py migrate --database=mysql_replica

### CrearSuperUser
python manage.py createsuperuser

### Configuracion Settings
Verificar que los puertos, usuario, sea la misma de sus claves en base de datos
Variable DATABASES
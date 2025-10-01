from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


"""
funcion para migracion 
python manage.py migrate --database=default
python manage.py migrate --database=mysql_replica
"""

from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    dpi = models.CharField(max_length=13, unique=True, null=True, blank=True) 
    second_last_name =  models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone_home = models.PositiveIntegerField(null=True, blank=True)
    phone_mobile = models.PositiveIntegerField(null=True, blank=True)
    salary = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    bonus = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Guardar en Postgres y MySQL con rollback en caso de fallo.
        """
        # Copia de kwargs para no modificar el original
        kwargs_copy = kwargs.copy()

        try:
            # Guardar en Postgres (default)
            kwargs_copy['using'] = 'default'
            super(User, self).save(*args, **kwargs_copy)

            # Guardar en MySQL (replica)
            kwargs_copy['using'] = 'mysql_replica'
            super(User, self).save(*args, **kwargs_copy)

        except Exception as e:
            # Rollback: eliminar de Postgres si ya estaba guardado
            try:
                super(User, self).delete(using='default')
            except Exception as rollback_error:
                print("Error al hacer rollback en Postgres:", rollback_error)

            print("Error al guardar usuario en MySQL:", e)
            raise e  # volvemos a lanzar el error para enterarnos

    def delete(self, *args, **kwargs):
        """
        Eliminar en Postgres y MySQL con rollback en caso de fallo.
        """
        kwargs_copy = kwargs.copy()
        user_id = self.id  # <- Guardamos el id ANTES de eliminar en Postgres

        # Copia de datos para rollback
        backup_data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
        }

        try:
            # Eliminar en Postgres
            kwargs_copy['using'] = 'default'
            super(User, self).delete(*args, **kwargs_copy)

            # Eliminar en MySQL usando el id guardado
            User.objects.using('mysql_replica').filter(id=user_id).delete()

        except Exception as e:
            # Rollback en Postgres: reinsertar o actualizar el usuario
            try:
                kwargs_copy['using'] = 'default'
                User.objects.using('default').update_or_create(
                    id=backup_data['id'], defaults=backup_data
                )
            except Exception as rollback_error:
                print("Error al hacer rollback en Postgres:", rollback_error)

            print("Error al eliminar usuario en MySQL:", e)
            raise e




class Registro(models.Model):
    ACCIONES = [
        ('add', 'Agregar'),
        ('edit', 'Editar'),
        ('delete', 'Eliminar'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    accion = models.CharField(max_length=10, choices=ACCIONES)
    modelo = models.CharField(max_length=100)  # Ejemplo: "User"
    objeto_id = models.CharField(max_length=100)  # ID del objeto afectado
    descripcion = models.TextField(blank=True, null=True)  # Detalles opcionales
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.accion} - {self.modelo}"
    
# senales para los registros
@receiver(post_save, sender=User)
def registrar_guardado(sender, instance, created, using, **kwargs):
    # Solo registrar desde la base principal para evitar duplicados
    accion = 'add' if created else 'edit'
    Registro.objects.create(
        usuario=instance,
        accion=accion,
        modelo=sender.__name__,
        objeto_id=instance.pk,
        descripcion=f"Usuario {instance.username} {'creado' if created else 'editado'} en {using}"
        )
@receiver(post_delete, sender=User)
def registrar_eliminado(sender, instance, using, **kwargs):
    Registro.objects.create(
            accion='delete',
            modelo=sender.__name__,
            objeto_id=instance.pk,
            descripcion=f"Usuario '{instance.username}' (ID {instance.pk}) eliminado en {using}"
        )
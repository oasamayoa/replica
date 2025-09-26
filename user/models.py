from django.db import models
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

        try:
            # Eliminar en Postgres
            kwargs_copy['using'] = 'default'
            super(User, self).delete(*args, **kwargs_copy)

            # Eliminar en MySQL
            kwargs_copy['using'] = 'mysql_replica'
            super(User, self).delete(*args, **kwargs_copy)

        except Exception as e:
            # Rollback: reinsertar en Postgres si no se logró borrar en MySQL
            try:
                kwargs_copy['using'] = 'default'
                super(User, self).save(*args, **kwargs_copy)
            except Exception as rollback_error:
                print("Error al hacer rollback en Postgres:", rollback_error)

            print("Error al eliminar usuario en MySQL:", e)
            raise e
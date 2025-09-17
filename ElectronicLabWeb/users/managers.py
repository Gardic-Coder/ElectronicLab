# users/managers.py
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, cedula, nombre, apellido, email=None, password=None, **extra_fields):
        if not cedula:
            raise ValueError("El usuario debe tener una cédula")
        if not nombre or not apellido:
            raise ValueError("El usuario debe tener nombre y apellido")

        user = self.model(
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            email=self.normalize_email(email) if email else None,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, nombre, apellido, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(cedula, nombre, apellido, email, password, **extra_fields)
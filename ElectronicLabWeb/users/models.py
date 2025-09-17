# users/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=[
        ('estudiante', 'Estudiante'),
        ('encargado', 'Encargado'),
        ('admin', 'Administrador')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('penalizado', 'Penalizado')
    ], default='activo')
    photo = models.ForeignKey('files.FileRecord', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_photos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cedula', 'nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
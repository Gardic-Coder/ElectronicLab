# users/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = PhoneNumberField(region='VE', blank=True, null=True)
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

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
    
    objects = UserManager()

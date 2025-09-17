# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('cedula', 'nombre', 'apellido', 'email', 'rol', 'estado', 'is_staff')
    list_filter = ('rol', 'estado', 'is_staff')
    fieldsets = (
        (None, {'fields': ('cedula', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'email', 'telefono')}),
        ('Permisos', {'fields': ('rol', 'estado', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula', 'nombre', 'apellido', 'email', 'telefono', 'rol', 'estado', 'password1', 'password2'),
        }),
    )
    search_fields = ('cedula', 'email', 'nombre', 'apellido')
    ordering = ('cedula',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)
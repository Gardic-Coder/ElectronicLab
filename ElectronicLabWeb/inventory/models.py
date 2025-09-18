from django.db import models
from files.models import FileRecord

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Component(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Ej: NE555
    description = models.TextField()  # Ej: "Integrado oscilador"
    stock = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)

    datasheet = models.ForeignKey(
        FileRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='datasheet_components'
    )
    image = models.ForeignKey(
        FileRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='image_components'
    )

    categories = models.ManyToManyField(Category, related_name='components')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.description}"
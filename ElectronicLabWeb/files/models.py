# files/models.py
from django.db import models
from django.utils import timezone

class FileRecord(models.Model):
    hash = models.CharField(max_length=64, unique=True)
    file = models.FileField(upload_to='uploads/')
    mime_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename
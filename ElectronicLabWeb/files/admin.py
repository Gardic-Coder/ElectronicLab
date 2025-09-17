# files/admin.py
from django.contrib import admin
from .models import FileRecord

admin.site.register(FileRecord)
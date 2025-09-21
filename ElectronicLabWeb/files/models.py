# files/models.py
import os
import hashlib
from PIL import Image
from django.db import models
from django.utils import timezone
from django.core.files.base import ContentFile
from dotenv import load_dotenv
import uuid

load_dotenv()

def parse_size(size_str):
    try:
        return tuple(map(int, size_str.lower().split('x')))
    except:
        return (800, 800)

def calculate_file_hash(file_obj):
    file_obj.seek(0)
    file_hash = hashlib.sha256(file_obj.read()).hexdigest()
    file_obj.seek(0)
    return file_hash

class FileRecord(models.Model):
    hash = models.CharField(max_length=64, unique=True)
    file = models.FileField(upload_to='uploads/originals/')
    mime_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True)
    preview = models.ImageField(upload_to='uploads/previews/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def _rename_file(self):
        ext = os.path.splitext(self.file.name)[1].lower()  # conserva extensión
        clean_name = f"{self.hash[:12]}_{uuid.uuid4().hex[:8]}{ext}"
        self.file.name = os.path.join('', clean_name)
        self.filename = clean_name


    def save(self, *args, **kwargs):
        # Calcular hash si no existe
        if not self.hash:
            self.hash = calculate_file_hash(self.file)
            #self.hash = hashlib.sha256(self.file.read()).hexdigest()
            #self.file.seek(0)

        # Renombrar archivo
        self._rename_file()

        # Detectar MIME
        self.mime_type = self.file.file.content_type
        self.filename = self.file.name

        # Validar MIME
        allowed_mimes = os.getenv('ALLOWED_MIME_TYPES', '').split(',')
        if self.mime_type not in allowed_mimes:
            raise ValueError(f"Tipo MIME no permitido: {self.mime_type}")

        # Procesar imagen si aplica
        if self.mime_type.startswith('image/'):
            image = Image.open(self.file)
            self._generate_resized_versions(image)

        # Procesar PDF (solo registrar)
        elif self.mime_type == 'application/pdf':
            self._process_pdf()

        super().save(*args, **kwargs)

    def _generate_resized_versions(self, image):
        base_name = os.path.splitext(os.path.basename(self.file.name))[0]
        ext = image.format.lower()
        thumb_name = f"{self.hash[:12]}_thumb.{ext}"
        preview_name = f"{self.hash[:12]}_preview.{ext}"

        thumb_size = parse_size(os.getenv('THUMBNAIL_SIZE', '100x100'))
        preview_size = parse_size(os.getenv('PREVIEW_SIZE', '800x800'))

        # Miniatura
        thumb = image.copy()
        thumb.thumbnail(thumb_size)
        thumb_io = ContentFile(b'')
        thumb.save(thumb_io, format=image.format)
        self.thumbnail.save(thumb_name, thumb_io, save=False)

        # Vista ampliada
        preview = image.copy()
        preview.thumbnail(preview_size)
        preview_io = ContentFile(b'')
        preview.save(preview_io, format=image.format)
        self.preview.save(preview_name, preview_io, save=False)

    def _process_pdf(self):
        # No se necesita procesamiento visual, solo registrar
        # Ya se detectó el MIME y se calculó el hash
        # Podés agregar lógica extra si querés extraer metadatos en el futuro
        pass
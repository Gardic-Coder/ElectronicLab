# files/management/commands/clean_orphans.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from files.models import FileRecord

class Command(BaseCommand):
    help = 'Elimina archivos huérfanos que no están referenciados en la base de datos'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        folders = ['uploads/originals', 'uploads/thumbnails', 'uploads/previews']

        # Obtener nombres de archivo referenciados
        referenced_names = set()
        for record in FileRecord.objects.all():
            if record.file:
                referenced_names.add(os.path.basename(record.file.name))
            if record.thumbnail:
                referenced_names.add(os.path.basename(record.thumbnail.name))
            if record.preview:
                referenced_names.add(os.path.basename(record.preview.name))

        deleted = 0
        scanned = 0

        for folder in folders:
            full_path = os.path.join(media_root, folder)
            if not os.path.exists(full_path):
                continue

            for filename in os.listdir(full_path):
                scanned += 1
                if filename not in referenced_names:
                    file_path = os.path.join(full_path, filename)
                    try:
                        os.remove(file_path)
                        deleted += 1
                        self.stdout.write(f"🗑️ Eliminado huérfano: {file_path}")
                    except Exception as e:
                        self.stderr.write(f"⚠️ Error al eliminar {file_path}: {e}")

        self.stdout.write(self.style.SUCCESS(f"✔️ Limpieza completada. Escaneados: {scanned}, Eliminados: {deleted}"))
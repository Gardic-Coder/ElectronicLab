from rest_framework import serializers
from .models import FileRecord

class FileRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRecord
        fields = ['id', 'file', 'mime_type', 'filename', 'thumbnail', 'preview', 'created_at']
        read_only_fields = ['mime_type', 'filename', 'thumbnail', 'preview', 'created_at']
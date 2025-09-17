# files/views.py
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import FileRecord

class FileUploadView(CreateView):
    model = FileRecord
    fields = ['file']
    template_name = 'files/upload.html'
    success_url = reverse_lazy('file_upload_success')
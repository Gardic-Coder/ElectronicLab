from django.urls import path
from .api_views import FileUploadAPI

urlpatterns = [
    path('upload/', FileUploadAPI.as_view(), name='api_file_upload'),
]
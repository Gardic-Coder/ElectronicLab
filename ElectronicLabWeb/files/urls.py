from django.urls import path
from .views import FileUploadView, FileUploadSuccessView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('success/', FileUploadSuccessView.as_view(), name='file_upload_success'),

]
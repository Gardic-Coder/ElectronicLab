from django.urls import path
from .views import ComponentListView, BulkDeleteView, ComponentCreateView, ComponentDetailView

app_name = 'inventory'

urlpatterns = [
    path('', ComponentListView.as_view(), name='list'),
    path('eliminar/', BulkDeleteView.as_view(), name='bulk_delete'),
    path('crear/', ComponentCreateView.as_view(), name='create'),
    path('detalle/<int:pk>/', ComponentDetailView.as_view(), name='component-detail'),
    # Puedes agregar otras vistas como:
    # path('crear/', ComponentCreateView.as_view(), name='create'),
]
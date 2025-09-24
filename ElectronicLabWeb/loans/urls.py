from django.urls import path
from .views import ConfirmarPrestamoView, CarritoPrestamoView, DetallePrestamoView, AgregarAlCarritoView

urlpatterns = [
    path('carrito/', CarritoPrestamoView.as_view(), name='ver_carrito'),
    path('confirmar/', ConfirmarPrestamoView.as_view(), name='confirmar_prestamo'),
    path('prestamo/<int:loan_id>/', DetallePrestamoView.as_view(), name='detalle_prestamo'),
    path('agregar/', AgregarAlCarritoView.as_view(), name='agregar_carrito'),
]
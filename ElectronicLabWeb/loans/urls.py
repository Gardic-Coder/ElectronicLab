from django.urls import path
from .views import (
    ConfirmarPrestamoView, CarritoPrestamoView, DetallePrestamoView, AgregarAlCarritoView,
    EliminarDelCarritoView, ActualizarCantidadCarritoView
)


urlpatterns = [
    path('carrito/', CarritoPrestamoView.as_view(), name='ver_carrito'),
    path('carrito/eliminar/', EliminarDelCarritoView.as_view(), name='eliminar_carrito'),
    path('carrito/actualizar/', ActualizarCantidadCarritoView.as_view(), name='actualizar_carrito'),
    path('carrito/confirmar/', ConfirmarPrestamoView.as_view(), name='confirmar_prestamo'),
    path('confirmar/', ConfirmarPrestamoView.as_view(), name='confirmar_prestamo'),
    path('prestamo/<int:loan_id>/', DetallePrestamoView.as_view(), name='detalle_prestamo'),
    path('agregar/', AgregarAlCarritoView.as_view(), name='agregar_carrito'),
]
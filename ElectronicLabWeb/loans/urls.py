from django.urls import path
from .views import (
    ConfirmarPrestamoView, CarritoPrestamoView, AgregarAlCarritoView,
    EliminarDelCarritoView, ActualizarCantidadCarritoView, LoanDashboardView, LoanDetailView,
    LoanAdminDashboardView, ProcesarPrestamoView
)


urlpatterns = [
    path('carrito/', CarritoPrestamoView.as_view(), name='ver_carrito'),
    path('carrito/eliminar/', EliminarDelCarritoView.as_view(), name='eliminar_carrito'),
    path('carrito/actualizar/', ActualizarCantidadCarritoView.as_view(), name='actualizar_carrito'),
    path('carrito/confirmar/', ConfirmarPrestamoView.as_view(), name='confirmar_prestamo'),
    path('dashboard/', LoanDashboardView.as_view(), name='dashboard'),
    path('prestamo/<int:pk>/', LoanDetailView.as_view(), name='detalle_prestamo'),
    path('admin/dashboard/', LoanAdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/procesar/<int:pk>/', ProcesarPrestamoView.as_view(), name='procesar_prestamo'),
    path('agregar/', AgregarAlCarritoView.as_view(), name='agregar_carrito'),
]
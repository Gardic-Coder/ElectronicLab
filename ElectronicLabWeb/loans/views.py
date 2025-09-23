# loans/views.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Loan, LoanComponent, LoanCart

class ConfirmarPrestamoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_items = LoanCart.objects.filter(user=request.user)
        if not cart_items.exists():
            # Puedes redirigir con un mensaje usando messages
            return redirect('inventory:component_list')

        loan = Loan.objects.create(user=request.user, fecha_solicitud=timezone.now())
        for item in cart_items:
            LoanComponent.objects.create(
                loan=loan,
                component=item.component,
                cantidad=item.cantidad
            )
            item.delete()

        return redirect('loans:detalle_prestamo', loan_id=loan.id)
    
class CarritoPrestamoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = LoanCart.objects.filter(user=request.user)
        return render(request, 'loans/cart_list.html', {'cart_items': cart_items})
    
class DetallePrestamoView(LoginRequiredMixin, View):
    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        return render(request, 'loans/loan_detail.html', {'loan': loan})
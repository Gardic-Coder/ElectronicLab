# loans/views.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Loan, LoanComponent, LoanCart
from inventory.models import Component
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic import TemplateView

class ConfirmarPrestamoView(LoginRequiredMixin, View):
    def post(self, request):
        cart_items = LoanCart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('ver_carrito')

        loan = Loan.objects.create(user=request.user, fecha_solicitud=timezone.now())
        for item in cart_items:
            LoanComponent.objects.create(
                loan=loan,
                component=item.component,
                cantidad=item.cantidad
            )
            item.delete()

        return redirect('detalle_prestamo', loan_id=loan.id)
    
class CarritoPrestamoView(LoginRequiredMixin, TemplateView):
    template_name = 'loans/cart_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = LoanCart.objects.filter(user=self.request.user).select_related('component')

        # Calcular disponibilidad por componente
        for item in cart_items:
            prestado = LoanComponent.objects.filter(
                component=item.component,
                loan__estado='aprobado'
            ).aggregate(total=Sum('cantidad'))['total'] or 0
            item.available = max(item.component.stock - prestado, 0)

        context['cart_items'] = cart_items
        return context
    
class DetallePrestamoView(LoginRequiredMixin, View):
    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        return render(request, 'loans/loan_detail.html', {'loan': loan})
    
class AgregarAlCarritoView(LoginRequiredMixin, View):
    def post(self, request):
        component_id = request.POST.get('component_id')
        cantidad = int(request.POST.get('cantidad', 1))

        component = Component.objects.filter(id=component_id).first()
        if not component:
            return JsonResponse({'error': 'Componente no encontrado'}, status=404)

        prestado = LoanComponent.objects.filter(
            component=component,
            loan__estado='aprobado'
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        disponible = max(component.stock - prestado, 0)

        if cantidad < 1 or cantidad > disponible:
            return JsonResponse({'error': 'Cantidad inválida o excede disponibilidad'}, status=400)

        cart_item, created = LoanCart.objects.update_or_create(
            user=request.user,
            component=component,
            defaults={'cantidad': cantidad}
        )

        return JsonResponse({'success': True, 'cantidad': cart_item.cantidad})

class EliminarDelCarritoView(LoginRequiredMixin, View):
    def post(self, request):
        component_id = request.POST.get('component_id')
        LoanCart.objects.filter(user=request.user, component_id=component_id).delete()
        return JsonResponse({'success': True})
    
class ActualizarCantidadCarritoView(LoginRequiredMixin, View):
    def post(self, request):
        component_id = request.POST.get('component_id')
        cantidad = int(request.POST.get('cantidad', 1))

        component = Component.objects.filter(id=component_id).first()
        if not component:
            return JsonResponse({'error': 'Componente no encontrado'}, status=404)

        prestado = LoanComponent.objects.filter(
            component=component,
            loan__estado='aprobado'
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        disponible = max(component.stock - prestado, 0)

        if cantidad < 1 or cantidad > disponible:
            return JsonResponse({'error': 'Cantidad inválida'}, status=400)

        LoanCart.objects.filter(user=request.user, component=component).update(cantidad=cantidad)
        return JsonResponse({'success': True})

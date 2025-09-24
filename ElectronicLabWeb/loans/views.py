# loans/views.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from .models import Loan, LoanComponent, LoanCart
from inventory.models import Component
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic import TemplateView, ListView

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

        return redirect('')
    
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
    
#class DetallePrestamoView(LoginRequiredMixin, View):
#    def get(self, request, loan_id, *args, **kwargs):
#        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
#        return render(request, 'loans/loan_detail.html', {'loan': loan})
    
class LoanDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        if loan.user != request.user and request.user.rol != 'encargado' and not request.user.is_staff:
            return JsonResponse({'error': 'No autorizado'}, status=403)
        items = loan.items.select_related('component').all()

        data = {
            'id': loan.id,
            'estado': loan.estado,
            'fecha_solicitud': loan.fecha_solicitud,
            'fecha_aprobacion': loan.fecha_aprobacion,
            'fecha_devolucion': loan.fecha_devolucion,
            'observaciones': loan.observaciones,
            'componentes': [
                {
                    'code': item.component.code,
                    'description': item.component.description,
                    'cantidad': item.cantidad
                } for item in items
            ]
        }
        return JsonResponse(data)

    
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

class LoanDashboardView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = 'loans/dashboard.html'
    context_object_name = 'loans'
    paginate_by = 10

    def get_queryset(self):
        estado = self.request.GET.get('estado')
        fecha = self.request.GET.get('fecha')
        qs = Loan.objects.filter(user=self.request.user).order_by('-fecha_solicitud')

        if estado:
            qs = qs.filter(estado=estado)

        if fecha:
            qs = qs.filter(fecha_solicitud=fecha)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ['pendiente', 'aprobado', 'rechazado', 'devuelto']
        context['selected_estado'] = self.request.GET.get('estado', '')
        context['selected_fecha'] = self.request.GET.get('fecha', '')
        return context

class LoanAdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Loan
    template_name = 'loans/admin_dashboard.html'
    context_object_name = 'loans'
    paginate_by = 10

    def test_func(self):
        return self.request.user.rol in ['encargado', 'admin'] or self.request.user.is_staff

    def get_queryset(self):
        estado = self.request.GET.get('estado', 'pendiente')
        fecha = self.request.GET.get('fecha')
        qs = Loan.objects.all().order_by('fecha_solicitud')

        if estado:
            qs = qs.filter(estado=estado)

        if fecha:
            qs = qs.filter(fecha_solicitud=fecha)

        return qs.select_related('user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = ['pendiente', 'aprobado', 'rechazado', 'devuelto']
        context['selected_estado'] = self.request.GET.get('estado', 'pendiente')
        context['selected_fecha'] = self.request.GET.get('fecha', '')
        return context
    
class ProcesarPrestamoView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.rol in ['encargado', 'admin'] or self.request.user.is_staff

    def post(self, request, pk):
        loan = get_object_or_404(Loan, pk=pk)
        estado = request.POST.get('estado')
        fecha_devolucion = request.POST.get('fecha_devolucion')
        observaciones = request.POST.get('observaciones', '')

        if estado not in ['aprobado', 'rechazado']:
            return JsonResponse({'error': 'Estado inválido'}, status=400)

        # Validar y actualizar cantidades
        for item in loan.items.all():
            nueva = int(request.POST.get(f'cantidad_{item.component.id}', item.cantidad))
            prestado = LoanComponent.objects.filter(
                component=item.component,
                loan__estado='aprobado'
            ).aggregate(total=Sum('cantidad'))['total'] or 0
            disponible = max(item.component.stock - prestado, 0)
            if nueva < 1 or nueva > disponible:
                return JsonResponse({'error': f'Cantidad inválida para {item.component.code}'}, status=400)
            item.cantidad = nueva
            item.save()

        loan.estado = estado
        loan.fecha_aprobacion = timezone.now()
        loan.fecha_devolucion = fecha_devolucion or None
        loan.motivo_rechazo = observaciones if estado == 'rechazado' else ''
        loan.encargado = request.user
        loan.save()

        return JsonResponse({'success': True})


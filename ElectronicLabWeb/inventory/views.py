# inventory/views.py
from django.views.generic import ListView
from django.db.models import Q
from .models import Component, Category
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views import View
from .forms import ComponentForm
from files.serializers import FileRecordSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.shortcuts import render

class ComponentListView(ListView):
    model = Component
    template_name = 'inventory/component_list.html'
    context_object_name = 'components'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        tags = self.request.GET.getlist('tags')
        qs = Component.objects.all()

        if query:
            qs = qs.filter(Q(code__icontains=query) | Q(description__icontains=query))

        if tags:
            qs = qs.filter(categories__name__in=tags).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['all_tags'] = Category.objects.all()
        context['all_tags_json'] = list(Category.objects.values('name'))
        return context
    
class BulkDeleteView(View):
    def post(self, request):
        ids = request.POST.getlist('selected')
        clave = request.POST.get('clave_confirmacion')

        user = authenticate(cedula=request.user.cedula, password=clave)
        if not user or not (user.rol == 'encargado' or user.is_staff):
            messages.error(request, "Clave incorrecta o permisos insuficientes.")
            return redirect('inventory:list')

        Component.objects.filter(id__in=ids).delete()
        messages.success(request, "Componentes eliminados correctamente.")
        return redirect('inventory:list')

class ComponentCreateView(View):
    def get(self, request):
        form = ComponentForm()
        return render(request, 'inventory/component_form.html', {'form': form})

    def post(self, request):
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            image_record = None
            datasheet_record = None

            # Subir imagen si se cargó
            if request.FILES.get('image_file'):
                image_record = self._save_file(request.FILES['image_file'])

            # Subir datasheet si se cargó
            if request.FILES.get('datasheet_file'):
                datasheet_record = self._save_file(request.FILES['datasheet_file'])

            # Crear componente
            component = form.save(commit=False)
            component.image = image_record
            component.datasheet = datasheet_record
            component.save()
            form.save_m2m()

            messages.success(request, "Componente creado exitosamente.")
            return redirect('inventory:list')
        return render(request, 'inventory/component_form.html', {'form': form})

    def _save_file(self, file_obj):
        factory = APIRequestFactory()
        drf_request = factory.post('/api/files/', {'file': file_obj}, format='multipart')
        request = Request(drf_request, parsers=[MultiPartParser()])
        serializer = FileRecordSerializer(data=request.data)
        if serializer.is_valid():
            return serializer.save()
        return None

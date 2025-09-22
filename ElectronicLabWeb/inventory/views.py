# inventory/views.py
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Component, Category
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views import View
from .forms import ComponentForm
from files.serializers import FileRecordSerializer
from files.models import FileRecord, calculate_file_hash
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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

        #print("IDs recibidos:", ids)
        #print("Clave recibida:", clave)
        user = authenticate(cedula=request.user.cedula, password=clave)
        if not user or not (user.rol == 'encargado' or user.is_staff):
            messages.error(request, "Clave incorrecta o permisos insuficientes.")
            return redirect('inventory:list')

        Component.objects.filter(id__in=ids).delete()
        messages.success(request, "Componentes eliminados correctamente.")
        return redirect('inventory:list')

class ComponentCreateView(CreateView):
    model = Component
    form_class = ComponentForm
    template_name = 'inventory/component_form.html'
    success_url = reverse_lazy('inventory:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags_json'] = list(Category.objects.values('name'))
        context['selected_tags'] = []
        return context

    def form_valid(self, form):
        image_record = self._save_file(self.request.FILES.get('image_file'))
        datasheet_record = self._save_file(self.request.FILES.get('datasheet_file'))

        tag_names = self.request.POST.getlist('tags')
        categories = [Category.objects.get_or_create(name=name.strip())[0] for name in tag_names]

        component = form.save(commit=False)
        component.image = image_record
        component.datasheet = datasheet_record
        component.save()
        component.categories.set(categories)
        form.save_m2m()

        messages.success(self.request, "Componente creado exitosamente.")
        return redirect(self.success_url)

    def _save_file(self, file_obj):
        if not file_obj:
            return None
        file_obj.seek(0)
        file_hash = calculate_file_hash(file_obj)

        # Verificar si ya existe
        existing = FileRecord.objects.filter(hash=file_hash).first()
        if existing:
            return existing

        # Si no existe, crear nuevo
        factory = APIRequestFactory()
        drf_request = factory.post('/api/files/', {'file': file_obj}, format='multipart')
        request = Request(drf_request, parsers=[MultiPartParser()])
        serializer = FileRecordSerializer(data=request.data)
        if serializer.is_valid():
            return serializer.save()
        return None

class ComponentDetailView(View):
    def get(self, request, pk):
        component = get_object_or_404(Component, pk=pk)
        image = component.image

        preview_url = image.preview.url if image and image.preview and image.preview.name else None
        thumbnail_url = image.thumbnail.url if image and image.thumbnail and image.thumbnail.name else None

        datasheet_url = component.datasheet.file.url if component.datasheet and component.datasheet.file.name else None

        data = {
            'code': component.code,
            'description': component.description,
            'stock': component.stock,
            'location': component.location,
            'categories': [cat.name for cat in component.categories.all()],
            'preview_url': preview_url,
            'thumbnail_url': thumbnail_url,
            'datasheet_url': datasheet_url,
            'can_edit': request.user.is_staff or getattr(request.user, 'rol', '') == 'encargado',
            'edit_url': reverse('inventory:component-edit', args=[component.pk]),
        }
        return JsonResponse(data)

class ComponentUpdateView(UpdateView):
    model = Component
    form_class = ComponentForm
    template_name = 'inventory/component_edit.html'
    success_url = reverse_lazy('inventory:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags_json'] = list(Category.objects.values('name'))
        context['selected_tags'] = [cat.name for cat in self.object.categories.all()]
        return context

    def form_valid(self, form):
        clave = self.request.POST.get('clave_confirmacion')
        if not self._validar_clave(clave):
            form.add_error(None, "Clave incorrecta para confirmar la edición.")
            return self.form_invalid(form)

        image_record = self._save_file(self.request.FILES.get('image_file'))
        datasheet_record = self._save_file(self.request.FILES.get('datasheet_file'))

        tag_names = self.request.POST.getlist('tags')
        categories = [Category.objects.get_or_create(name=name.strip())[0] for name in tag_names]

        component = form.save(commit=False)
        component.image = image_record or component.image
        component.datasheet = datasheet_record or component.datasheet
        component.save()
        component.categories.set(categories)
        form.save_m2m()

        messages.success(self.request, "Componente editado exitosamente.")
        return redirect(self.success_url)

    def _validar_clave(self, clave):
        return clave == "clave_segura"  # reemplaza por tu lógica real

    def _save_file(self, file_obj):
        if not file_obj:
            return None
        file_obj.seek(0)
        file_hash = calculate_file_hash(file_obj)

        # Verificar si ya existe
        existing = FileRecord.objects.filter(hash=file_hash).first()
        if existing:
            return existing

        # Si no existe, crear nuevo
        factory = APIRequestFactory()
        drf_request = factory.post('/api/files/', {'file': file_obj}, format='multipart')
        request = Request(drf_request, parsers=[MultiPartParser()])
        serializer = FileRecordSerializer(data=request.data)
        if serializer.is_valid():
            return serializer.save()
        return None

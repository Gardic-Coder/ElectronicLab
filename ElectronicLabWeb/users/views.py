from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from .models import User
from .forms import UserProfileForm
from files.serializers import FileRecordSerializer
from files.models import FileRecord, calculate_file_hash
from django.contrib.auth import update_session_auth_hash
from django.views import View

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        clave = self.request.POST.get('clave_confirmacion')
        if not self.request.user.check_password(clave):
            form.add_error(None, "Contraseña incorrecta para confirmar los cambios.")
            return self.form_invalid(form)

        user = form.save(commit=False)

        if self.request.POST.get('delete_photo') == 'on':
            user.photo = None

        photo_file = self.request.FILES.get('photo_file')
        if photo_file:
            user.photo = self._save_file(photo_file)

        user.save()
        messages.success(self.request, "Perfil actualizado correctamente.")
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user  # ← asegúrate de esto
        return context

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if new == current:
            messages.error(request, "La nueva contraseña no puede ser igual a la actual.")
        elif new != confirm:
            messages.error(request, "La confirmación no coincide con la nueva contraseña.")
        elif not request.user.check_password(current):
            messages.error(request, "La contraseña actual es incorrecta.")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Contraseña actualizada correctamente.")

        return redirect('profile')

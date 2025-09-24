from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserProfileUpdateView, UserProfileView, ChangePasswordView, PerfilUsuarioView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/editar/', UserProfileUpdateView.as_view(), name='profile-edit'),
    path('perfil/', UserProfileView.as_view(), name='profile'),
    path('perfil/cambiar-clave/', ChangePasswordView.as_view(), name='change-password'),
    path('perfil/<int:pk>/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
]
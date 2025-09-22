from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserProfileUpdateView, UserProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/editar/', UserProfileUpdateView.as_view(), name='profile-edit'),
    path('perfil/', UserProfileView.as_view(), name='profile'),
]
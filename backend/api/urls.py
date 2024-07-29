from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('usuario/<int:usuario_id>/', views.UsuarioPerfilView.as_view(), name='usuario_perfil'),
    path('usuarios/', views.UsuariosView.as_view(), name='usuarios'),
]

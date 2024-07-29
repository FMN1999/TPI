from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/usuario/<int:id>', views.usuario, name='usuario'),
    path('testing/', views.testing, name='testing'),
]
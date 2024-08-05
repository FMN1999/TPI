from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('usuario/<int:usuario_id>/', views.UsuarioPerfilView.as_view(), name='usuario_perfil'),
    path('usuarios/', views.UsuariosView.as_view(), name='usuarios'),
    path('crear-equipo/', views.CrearEquipoView.as_view(), name='crear_equipo'),
    path('dts/', views.ObtenerDTsView.as_view(), name='dts'),
    path('asistentes/', views.ObtenerAsistentesView.as_view(), name='asistentes'),
    path('jugadores/', views.ObtenerJugadoresView.as_view(), name='jugadores'),
    path('equipos/', views.EquiposView.as_view(), name='equipos_list'),
    path('equipos/<int:equipo_id>/', views.CrearEquipoView.as_view(), name='equipo_detail'),
]

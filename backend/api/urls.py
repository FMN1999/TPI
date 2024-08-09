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
    path('crear-liga/', views.CrearLigaView.as_view(), name='crear_liga'),
    path('ligas/', views.LigasView.as_view(), name='todas_las_ligas'),
    path('ligas/<int:liga_id>/', views.LigaView.as_view(), name='obtener_liga'),
    path('liga/<int:liga_id>/temporadas/', views.TemporadasPorLigaView.as_view(), name='listar_temporadas'),
    path('temporada/crear/', views.CrearTemporadaView.as_view(), name='crear_temporada'),
    #path('temporadas/', views.TemporadasView.as_view(), name='temporadas'),
    path('temporada/<int:id>/', views.TemporadaDetailView.as_view(), name='temporada_detail'),
    path('posiciones/<int:temporada_id>/', views.PosicionesView.as_view(), name='posiciones'),
    path('posiciones/', views.PosicionesView.as_view(), name='agregar_posicion'),
    path('partido/', views.PartidosView.as_view(), name='agregar_partido'),
    path('partido/<int:temporada_id>/', views.PartidosView.as_view(), name='get_partidos_por_temporada'),
]

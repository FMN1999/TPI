from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .controller import *


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            usuario = UsuarioController.registrar_usuario(data)
            return JsonResponse({'message': 'Usuario registrado con éxito', 'id': usuario.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            usuario = data.get('usuario')
            contrasenia = data.get('contrasenia')
            usuario_obj = UsuarioController.autenticar_usuario(usuario, contrasenia)
            if usuario_obj:
                response_data = {
                    'token': 'fake-token',  # Aquí normalmente se devolvería un token real.
                    'user_id': usuario_obj.id
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UsuarioPerfilView(View):
    def get(self, request, usuario_id):
        usuario = UsuarioController.obtener_usuario_por_id(usuario_id)
        if usuario:
            return JsonResponse({
                'id': usuario.id,
                'usuario': usuario.usuario,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'sexo': usuario.sexo,
                'fecha_nacimiento': usuario.fecha_nacimiento,
                'ciudad_nacimiento': usuario.ciudad_nacimiento,
                'provincia_nacimiento': usuario.provincia_nacimiento
            })
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)


class UsuariosView(View):
    def get(self, request):
        usuarios = UsuarioController.obtener_todos_usuarios()
        usuarios_list = [{
            'id': usuario.id,
            'usuario': usuario.usuario,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido
        } for usuario in usuarios]
        return JsonResponse(usuarios_list, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class EquiposView(View):
    def get(self, request):
        equipos = EquipoController.fetch_all_equipos()
        equipos_data = [
            {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'logo': equipo.logo,
                'direccion': equipo.direccion,
                'ciudad': equipo.ciudad,
                'provincia': equipo.provincia,
                'cant_victorias_local': equipo.cant_victorias_local,
                'cant_victorias_visit': equipo.cant_victorias_visit,
                'campeonatos': equipo.campeonatos,
                'campeones_actuales': equipo.campeones_actuales,
            }
            for equipo in equipos
        ]
        return JsonResponse(equipos_data, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class CrearEquipoView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            equipo = EquipoController.crear_equipo_con_miembros(data)
            return JsonResponse({'message': 'Equipo registrado con éxito', 'id': equipo.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request, equipo_id):
        equipo = EquipoController.fetch_equipo_by_id(equipo_id)
        if equipo is None:
            return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
        equipo_data = {
            'id': equipo.id,
            'nombre': equipo.nombre,
            'logo': equipo.logo,
            'direccion': equipo.direccion,
            'ciudad': equipo.ciudad,
            'provincia': equipo.provincia,
            'cant_victorias_local': equipo.cant_victorias_local,
            'cant_victorias_visit': equipo.cant_victorias_visit,
            'campeonatos': equipo.campeonatos,
            'campeones_actuales': equipo.campeones_actuales,
        }
        return JsonResponse(equipo_data)


class ObtenerDTsView(View):
    def get(self, request):
        dt_list = []
        dts = UsuarioController.obtener_dts()
        for dt in dts:
            usuario = UsuarioController.obtener_usuario_por_id(dt.id_usuario.id)
            dt_list.append(
                {'id': dt.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido, 'telefono': dt.telefono})
        return JsonResponse(dt_list, safe=False)


class ObtenerAsistentesView(View):
    def get(self, request):
        asistente_list = []
        asistentes = UsuarioController.obtener_asistentes()
        for asistente in asistentes:
            usuario = UsuarioController.obtener_usuario_por_id(asistente.id_usuario.id)
            asistente_list.append({'id': asistente.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido})
        return JsonResponse(asistente_list, safe=False)


class ObtenerJugadoresView(View):
    def get(self, request):
        jugador_list = []
        jugadores = UsuarioController.obtener_jugadores()
        for jugador in jugadores:
            usuario = UsuarioController.obtener_usuario_por_id(jugador.id_usuario.id)
            jugador_list.append(
                {'id': jugador.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido, 'altura': jugador.altura,
                 'peso': jugador.peso})
        return JsonResponse(jugador_list, safe=False)


class CrearLigaView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            categoria = data.get('categoria')
            ptos_x_victoria = data.get('ptos_x_victoria')
            ptos_x_32_vict = data.get('ptos_x_32_vict')
            ptos_x_32_derrota = data.get('ptos_x_32_derrota')

            liga = LigaController.crear_liga(categoria, ptos_x_victoria, ptos_x_32_vict, ptos_x_32_derrota)
            return JsonResponse(liga.to_dict(), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LigasView(View):
    def get(self, request):
        try:
            ligas = LigaController.obtener_todas_las_ligas()
            ligas_data = [liga.to_dict() for liga in ligas]
            return JsonResponse(ligas_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LigaView(View):
    def get(self, request, liga_id):
        try:
            liga = LigaController.obtener_liga_por_id(liga_id)
            if liga:
                return JsonResponse(liga.to_dict(), safe=False)
            else:
                return JsonResponse({'error': 'Liga no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
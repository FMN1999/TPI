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
                    'user_id': usuario_obj.id  # Devolver el ID del usuario
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


@method_decorator(csrf_exempt, name='dispatch')
class CrearLigaView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            liga = LigaController.crear_liga(data)
            return JsonResponse({'message': 'Liga registrada con éxito', 'id': liga.id}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LigasView(View):
    def get(self, request):
        try:
            ligas = LigaController.obtener_todas_las_ligas()
            ligas_data = [
                {
                    'id': liga.id,
                    'categoria': liga.categoria,
                    'ptos_x_victoria': liga.ptos_x_victoria,
                    'ptos_x_32_vict': liga.ptos_x_32_vict,
                    'ptos_x_32_derrota': liga.ptos_x_32_derrota
                }
                for liga in ligas]
            return JsonResponse(ligas_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LigaView(View):
    def get(self, request, liga_id):
        try:
            liga = LigaController.obtener_liga_por_id(liga_id)
            liga_data = {
                            'id': liga.id,
                            'categoria': liga.categoria,
                            'ptos_x_victoria': liga.ptos_x_victoria,
                            'ptos_x_32_vict': liga.ptos_x_32_vict,
                            'ptos_x_32_derrota': liga.ptos_x_32_derrota
                         }
            if liga:
                return JsonResponse(liga_data, safe=False)
            else:
                return JsonResponse({'error': 'Liga no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class TemporadasPorLigaView(View):
    def get(self, request, liga_id):
        try:
            temporadas = TemporadaController.obtener_temporadas_por_liga(liga_id)
            temporadas_data = [
                {
                    'id': temporada.id,
                    'anio_desde': temporada.anio_desde,
                    'anio_hasta': temporada.anio_hasta,
                    'estado': temporada.estado,
                    'id_liga': temporada.id_liga.id
                }
                for temporada in temporadas
            ]
            return JsonResponse(temporadas_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CrearTemporadaView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nueva_temporada = TemporadaController.crear_temporada(data)
            temporada_data = {
                'id': nueva_temporada.id,
                'anio_desde': nueva_temporada.anio_desde,
                'anio_hasta': nueva_temporada.anio_hasta,
                'estado': nueva_temporada.estado,
                'id_liga': nueva_temporada.id_liga.id
            }
            return JsonResponse(temporada_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PosicionesView(View):
    def get(self, request, temporada_id):
        try:
            posiciones = PosicionesController.obtener_posiciones(temporada_id)
            posiciones_data = [
                {
                    'id': posicion.id,
                    'id_equipo': posicion.id_equipo.id,
                    'id_temporada': posicion.id_temporada.id,
                    'puntaje': posicion.puntaje,
                    'set_ganados': posicion.set_ganados,
                    'set_en_contra': posicion.set_en_contra,
                    'diferencia_sets': posicion.diferencia_sets
                }
                for posicion in posiciones
            ]
            return JsonResponse(posiciones_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        try:
            data = json.loads(request.body)
            id_equipo = data['id_equipo']
            id_temporada = data['id_temporada']
            posicion = PosicionesController.agregar_equipo(id_equipo, id_temporada)
            posicion_data = {
                'id': posicion.id,
                'id_equipo': posicion.id_equipo.id,
                'id_temporada': posicion.id_temporada.id,
                'puntaje': posicion.puntaje,
                'set_ganados': posicion.set_ganados,
                'set_en_contra': posicion.set_en_contra,
                'diferencia_sets': posicion.diferencia_sets
            }
            return JsonResponse(posicion_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class TemporadaDetailView(View):
    def get(self, request, id):
        try:
            temporada = TemporadaController.obtener_temporada(id)
            temporada_data = {
                'id': temporada.id,
                'anio_desde': temporada.anio_desde,
                'anio_hasta': temporada.anio_hasta,
                'estado': temporada.estado,
                'id_liga': temporada.id_liga.id
            }
            return JsonResponse(temporada_data, safe=False)
        except Temporada.DoesNotExist:
            return JsonResponse({'error': 'Temporada no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PartidosView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            partido = PartidoController.agregar_partido(data)
            return JsonResponse({'id': partido.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, temporada_id):
        try:
            partidos = PartidoController.obtener_partidos_por_temporada(temporada_id)
            partidos_data = [
                {
                    'id': partido.id,
                    'id_local': partido.id_local_id,
                    'id_visita': partido.id_visita_id,
                    'fecha': partido.fecha,
                    'hora': partido.hora,
                    'set_ganados_local': partido.set_ganados_local,
                    'set_ganados_visita': partido.set_ganados_visita,
                    'id_temporada': partido.id_temporada_id
                }
                for partido in partidos
            ]
            return JsonResponse(partidos_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class CrearFormacionView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            formacion = FormacionController.crear_formacion(data)
            return JsonResponse({'success': True, 'formacion_id': formacion.id}, status=201)
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


class EquipoJugadorView(View):
    def get(self, request, equipo_id):
        # Obtener todos los registros de EquipoJugador para el id_equipo
        equipo_jugadores = EquipoJugadorController.obtener_jugadores_por_equipo(equipo_id)

        if equipo_jugadores:
            # Crear una lista para almacenar los datos de los jugadores
            jugadores_list = [
                {
                    'id': ej.id_jugador.id,
                    'nombre': ej.id_jugador.id_usuario.nombre,
                    'apellido': ej.id_jugador.id_usuario.apellido,
                    'altura': ej.id_jugador.altura,
                    'peso': ej.id_jugador.peso
                }
                for ej in equipo_jugadores
            ]
            return JsonResponse(jugadores_list, safe=False)

        return JsonResponse({'error': 'No se encontraron jugadores para el equipo especificado'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class SetView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            # Llama al controlador para manejar la lógica de creación del set
            resultado = SetController.crear_set_controller(data)

            if 'error' in resultado:
                return JsonResponse({'error': resultado['error']}, status=400)

            return JsonResponse({'success': True, 'partido': resultado['partido']}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class PartidosSinSetsGanadosView(View):
    def get(self, request, *args, **kwargs):
        partidos = Partido.objects.filter(set_ganados_local=0, set_ganados_visita=0)
        data = list(partidos.values())
        return JsonResponse(data, safe=False)


class DetallePartidoView(View):
    def get(self, request, id_partido):
        detalles = PartidoController.ver_detalles_partido(id_partido)
        if detalles:
            return JsonResponse(detalles, safe=False, status=200)
        return JsonResponse({"error": "Partido no encontrado"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AgregarSetView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nuevo_set = SetController.agregar_set(data)

            if nuevo_set:
                return JsonResponse({"success": "Set agregado exitosamente"}, status=201)
            return JsonResponse({"error": "No se pudo agregar el set"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON malformado"}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Falta el campo {str(e)}"}, status=400)
        except Exception as e:
            print(f"Error inesperado: {e}")  # Añade este log para errores inesperados
            return JsonResponse({"error": "Error inesperado"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TerminarPartidoView(View):
    def post(self, request):
        data = request.POST
        id_partido = data.get('id_partido')
        resultado = PartidoController.terminar_partido(id_partido)
        if resultado:
            return JsonResponse({"message": "Partido terminado con éxito"}, status=200)
        return JsonResponse({"error": "No se pudo terminar el partido"}, status=400)


class ObtenerFormacionesView(View):
    def get(self, request, id_equipo):
        formaciones = FormacionController.obtener_formaciones_equipo(id_equipo)
        if formaciones is not None:
            # Construimos la lista de diccionarios en la vista
            form_list = [
                {
                    "id": f.id,
                    "id_equipo": f.id_equipo.id,
                    "jugador_1": f.jugador_1.id_usuario.nombre,
                    "jugador_2": f.jugador_2.id_usuario.nombre,
                    "jugador_3": f.jugador_3.id_usuario.nombre,
                    "jugador_4": f.jugador_4.id_usuario.nombre,
                    "jugador_5": f.jugador_5.id_usuario.nombre,
                    "jugador_6": f.jugador_6.id_usuario.nombre,
                    "libero": f.libero.id_usuario.nombre
                }
                for f in formaciones
            ]
            print(form_list)
            return JsonResponse(form_list, safe=False)

        return JsonResponse({"error": "No se pudieron obtener los sets"}, status=400)



class ObtenerSetsPorPartidoView(View):
    def get(self, request, id_partido):
        sets = SetController.obtener_sets_por_partido(id_partido)

        if sets is not None:
            # Construimos la lista de diccionarios en la vista
            sets_list = [
                {
                    "id": s.id,
                    "id_partido": s.id_partido.id,
                    "puntos_local": s.puntos_local,
                    "puntos_visita": s.puntos_visita,
                    "id_formacion_local": {
                        "id": s.id_formacion_local.id,
                        "jugador_1": s.id_formacion_local.jugador_1.id,
                        "jugador_2": s.id_formacion_local.jugador_2.id,
                        "jugador_3": s.id_formacion_local.jugador_3.id,
                        "jugador_4": s.id_formacion_local.jugador_4.id,
                        "jugador_5": s.id_formacion_local.jugador_5.id,
                        "jugador_6": s.id_formacion_local.jugador_6.id,
                        "libero": s.id_formacion_local.libero.id if s.id_formacion_local.libero else None
                    } if s.id_formacion_local else None,
                    "id_formacion_visit": {
                        "id": s.id_formacion_visit.id,
                        "jugador_1": s.id_formacion_visit.jugador_1.id,
                        "jugador_2": s.id_formacion_visit.jugador_2.id,
                        "jugador_3": s.id_formacion_visit.jugador_3.id,
                        "jugador_4": s.id_formacion_visit.jugador_4.id,
                        "jugador_5": s.id_formacion_visit.jugador_5.id,
                        "jugador_6": s.id_formacion_visit.jugador_6.id,
                        "libero": s.id_formacion_visit.libero.id if s.id_formacion_visit.libero else None
                    } if s.id_formacion_visit else None,
                }
                for s in sets
            ]
            return JsonResponse(sets_list, safe=False)

        return JsonResponse({"error": "No se pudieron obtener los sets"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RegistrarCambioView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            response_data = CambioController.registrar_cambio(data)
            return JsonResponse(response_data, status=201)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class EstadisticasView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            estadistica = EstadisticasController.registrar_estadisticas_controller(data)
            return JsonResponse({'mensaje': 'Estadísticas registradas exitosamente'})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error al registrar las estadísticas'}, status=500)
        
    
class CompruebaUsuario(View):
    def get(self, request, usuario_id):
        tipo_usuario = UsuarioController.obtener_tipo_usuario(usuario_id)
        return JsonResponse({'tipo': tipo_usuario})
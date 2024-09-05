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
            # Verificar si ya existe un usuario con el mismo usuario o email
            if UsuarioController.usuario_existe(data):
                return JsonResponse({'error': 'El nombre de usuario o email ya está en uso'}, status=400)

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


@method_decorator(csrf_exempt, name='dispatch')
class UsuarioPerfilView(View):
    def get(self, request, usuario_id):
        usuario = UsuarioController.obtener_usuario_por_id(usuario_id)
        adic = UsuarioController.obtiene_datos_completos(usuario_id)
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
                'provincia_nacimiento': usuario.provincia_nacimiento,
                'peso': adic.get('peso'),
                'altura': adic.get('altura'),
                'telefono': adic.get('telefono')
            })
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    def put(self, request, usuario_id):
        data = json.loads(request.body)
        usuario_actualizado = UsuarioController.actualizar_usuario(usuario_id, data)

        if usuario_actualizado:
            tipo_usuario = UsuarioController.obtener_tipo_usuario(usuario_id)

            if tipo_usuario == 'D':
                UsuarioController.actualizar_dt(usuario_id, data)
            elif tipo_usuario == 'J':
                UsuarioController.actualizar_jugador(usuario_id, data)

            return JsonResponse({'mensaje': 'Usuario actualizado correctamente'})

        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)


class UsuariosView(View):
    def get(self, request):
        usuarios_list = UsuarioController.obtener_todos_usuarios()
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
            # Verificar si ya existe un equipo con el mismo nombre
            if EquipoController.equipo_existe(data):
                return JsonResponse({'error': f"Ya existe un equipo con el nombre '{data.get('nombre')}'"}, status=400)

            equipo = EquipoController.crear_equipo_con_miembros(data)
            return JsonResponse({'message': 'Equipo registrado con éxito', 'id': equipo.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request, equipo_id):
        equipo_completo = EquipoController.obtener_equipo_completo(equipo_id)
        if not equipo_completo:
            return JsonResponse({'error': 'Equipo no encontrado'}, status=404)

        equipo = equipo_completo['equipo']
        dts = equipo_completo['dts']
        asistentes = equipo_completo['asistentes']
        jugadores = equipo_completo['jugadores']

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
            'dts': [{'id': dt.id_dt.id, 'nombre': dt.id_dt.id_usuario.nombre, 'apellido': dt.id_dt.id_usuario.apellido} for dt
                    in dts],
            'asistentes': [{'id': asistente.id_asistente.id, 'nombre': asistente.id_asistente.id_usuario.nombre,
                            'apellido': asistente.id_asistente.id_usuario.apellido} for asistente in asistentes],
            'jugadores': [{'id': jugador.id_jugador.id, 'nombre': jugador.id_jugador.id_usuario.nombre,
                           'apellido': jugador.id_jugador.id_usuario.apellido, 'nro_jugador': jugador.nro_jugador,
                           'posicion_pcpal': jugador.posicion_pcpal} for jugador in jugadores],
        }
        return JsonResponse(equipo_data)


@method_decorator(csrf_exempt, name='dispatch')
class AgregarAsistenteView(View):
    def post(self, request, equipo_id, asistente_id):
        try:
            EquipoController.agregar_asistente_a_equipo(equipo_id, asistente_id)
            return JsonResponse({'message': 'Asistente agregado con éxito'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AgregarDTView(View):
    def post(self, request, equipo_id, dt_id):
        try:
            EquipoController.agregar_dt_a_equipo(equipo_id, dt_id)
            return JsonResponse({'message': 'DT agregado con éxito'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AgregarJugadorView(View):
    def post(self, request, equipo_id, jugador_id):
        try:
            data = json.loads(request.body)
            nro_jugador = data.get('nro_jugador')
            posicion_pcpal = data.get('posicion_pcpal')
            posicion_secundaria = data.get('posicion_secundaria')
            EquipoController.agregar_jugador_a_equipo(equipo_id, jugador_id, nro_jugador, posicion_pcpal, posicion_secundaria)
            return JsonResponse({'message': 'Jugador agregado con éxito'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DarDeBajaView(View):
    def post(self, request, equipo_id,tipo, miembro_id):
        try:
            if EquipoController.dar_de_baja_miembro(equipo_id, tipo, miembro_id):
                return JsonResponse({'message': 'Miembro dado de baja con éxito'}, status=200)
            else:
                return JsonResponse({'error': 'Miembro no encontrado o tipo no válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
            if LigaController.liga_existe(data):
                return JsonResponse({'error': f"Ya existe una liga con el nombre '{data.get('nombre')}'"}, status=400)
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
                    'nombre': liga.nombre,
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
                'nombre': liga.nombre,
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


@method_decorator(csrf_exempt, name='dispatch')
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

    def delete(self, request, id):
        try:
            eliminado = TemporadaController.eliminar_temporada(id)
            if eliminado:
                return JsonResponse({'message': 'Temporada eliminada con éxito'}, status=200)
            else:
                return JsonResponse({'error': 'Temporada no encontrada'}, status=404)
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
                    'nombre': posicion.id_equipo.nombre,
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

    def delete(self, request, id):
        try:
            resultado = PosicionesController.eliminar_posicion(id)
            if 'error' in resultado:
                return JsonResponse({'error': resultado['error']}, status=400)
            return JsonResponse({'message': 'Posición eliminada con éxito'}, status=200)
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
                    'local': partido.id_local.nombre,
                    'visita': partido.id_visita.nombre,
                    'fecha': partido.fecha,
                    'hora': partido.hora,
                    'set_ganados_local': partido.set_ganados_local,
                    'set_ganados_visita': partido.set_ganados_visita,
                    'id_temporada': partido.id_temporada_id,
                    'logo_local': partido.id_local.logo,
                    'logo_visita': partido.id_visita.logo
                }
                for partido in partidos
            ]
            return JsonResponse(partidos_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, partido_id):
        try:
            eliminado = PartidoController.eliminar_partido_si_puntaje_cero(partido_id)
            if eliminado:
                return JsonResponse({'message': 'Partido eliminado con éxito'}, status=200)
            else:
                return JsonResponse({'error': 'No se puede eliminar el partido porque los sets ganados no son cero'},
                                    status=400)
        except Partido.DoesNotExist:
            return JsonResponse({'error': 'Partido no encontrado'}, status=404)
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


class PartidosSinSetsGanadosView(View):
    def get(self, request, *args, **kwargs):
        partidos = PartidoController.get_partidos_sin_sets()

        data = [
            {
                'id': partido.id,
                'local': partido.id_local.nombre,
                'visita': partido.id_visita.nombre,
                'fecha': partido.fecha,
                'hora': partido.hora,
                'logo_local': partido.id_local.logo,
                'logo_visita': partido.id_visita.logo,
                'nombre_liga': partido.id_temporada.id_liga.nombre,
                'categoria': partido.id_temporada.id_liga.categoria
            }
            for partido in partidos
        ]

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

    def delete(self, request, id_set):
        try:
            resultado = SetController.eliminar_set(id_set)
            if "error" in resultado:
                return JsonResponse({"error": resultado["error"]}, status=404)
            return JsonResponse({"mensaje": resultado["mensaje"]}, status=200)
        except Exception as e:
            print(f"Error al eliminar set: {e}")
            return JsonResponse({"error": "Error al eliminar el set"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TerminarPartidoView(View):
    def post(self, request):
        data = request.POST
        id_partido = data.get('id_partido')
        print(id_partido)
        resultado = PartidoController.terminar_partido(id_partido)
        if resultado:
            return JsonResponse({"message": "Partido terminado con éxito"}, status=200)
        return JsonResponse({"error": "No se pudo terminar el partido"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ObtenerFormacionesView(View):
    def get(self, request, id_equipo):
        print(id_equipo)
        formaciones = FormacionController.obtener_formaciones_equipo(id_equipo)
        print(formaciones)
        if formaciones is not None:
            # Construimos la lista de diccionarios en la vista
            form_list = [
                {
                    "id": f.id,
                    "id_equipo": f.id_equipo.id,
                    "jugador_1": str(f.jugador_1.id_usuario.nombre + ' ' + f.jugador_1.id_usuario.apellido),
                    "jugador_2": str(f.jugador_2.id_usuario.nombre + ' ' + f.jugador_2.id_usuario.apellido),
                    "jugador_3": str(f.jugador_3.id_usuario.nombre + ' ' + f.jugador_3.id_usuario.apellido),
                    "jugador_4": str(f.jugador_4.id_usuario.nombre + ' ' + f.jugador_4.id_usuario.apellido),
                    "jugador_5": str(f.jugador_5.id_usuario.nombre + ' ' + f.jugador_5.id_usuario.apellido),
                    "jugador_6": str(f.jugador_6.id_usuario.nombre + ' ' + f.jugador_6.id_usuario.apellido),
                    "libero": str(f.libero.id_usuario.nombre + ' ' + f.libero.id_usuario.apellido)
                }
                for f in formaciones
            ]
            print(form_list)
            return JsonResponse(form_list, safe=False)

        return JsonResponse({"error": "No se pudieron obtener los sets"}, status=400)

    def delete(self, request, id_formacion):
        FormacionController.eliminar_formacion(id_formacion)
        return JsonResponse({'message': 'Formación eliminada con éxito'})


class EquiposFueraDeTemporadaView(View):
    def get(self, request, temporada_id):
        try:
            equipos = EquipoController.obtener_equipos_fuera_de_temporada(temporada_id)
            equipos_data = [{'id': equipo.id, 'nombre': equipo.nombre} for equipo in equipos]
            return JsonResponse(equipos_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


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

    def get(self, request, id_partido):
        try:
            cambios = CambioController.obtener_cambios_por_partido(id_partido)
            return JsonResponse(cambios, safe = False)
        except Exception as e:
            print(f"Error: {str(e)}")  # Se agrega un print para verificar el error
            return JsonResponse({'error': 'Error al registrar las estadísticas'}, status=500)


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

    def get(self, request, jugador_id):
        try:
            print(jugador_id)
            estadisticas = EstadisticasController.obtener_estadisticas_por_jugador(jugador_id)
            if estadisticas:
                return JsonResponse(estadisticas, safe=False)
            else:
                return JsonResponse({"error": "Estadísticas no encontradas"}, status=404)
        except Exception as e:
            print(f"Error: {str(e)}")  # Se agrega un print para verificar el error
            return JsonResponse({"error": str(e)}, status=500)


class CompruebaUsuario(View):
    def get(self, request, usuario_id):
        tipo_usuario = UsuarioController.obtener_tipo_usuario(usuario_id)
        return JsonResponse({'tipo': tipo_usuario})


class VerificarAsistenteView(View):
    def get(self, request, id_equipo, id_usuario):
        es_asistente = EquipoController.verificar_asistente_equipo(id_usuario, id_equipo)
        return JsonResponse({'es_asistente': es_asistente})


class VerificarDtView(View):
    def get(self, request, id_equipo, id_usuario):
        es_dt = EquipoController.verificar_dt_equipo(id_usuario, id_equipo)
        return JsonResponse({'es_dt': es_dt})
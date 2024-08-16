from .db import *
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def convertir_fecha(fecha_str):
    if fecha_str is None:
        return None
    try:
        fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
        return fecha.date()
    except ValueError:
        logger.error(f"Fecha inválida: {fecha_str}")
        return None


class UsuarioController:
    @staticmethod
    def iniciar_sesion(usuario, contrasenia):
        usuario_obj = UsuarioData.obtener_usuario_por_usuario(usuario)
        if usuario_obj and usuario_obj.contrasenia == contrasenia:
            return usuario_obj
        return None

    @staticmethod
    def registrar_usuario(data):
        usuario = UsuarioData.crear_usuario(data)
        tipo_usuario = data.get('tipo_usuario')
        if tipo_usuario == 'Asistente':
            UsuarioData.crear_asistente(usuario)
        elif tipo_usuario == 'DT':
            telefono = data.get('telefono')
            UsuarioData.crear_dt(usuario, telefono)
        elif tipo_usuario == 'Jugador':
            altura = data.get('altura')
            peso = data.get('peso')
            UsuarioData.crear_jugador(usuario, altura, peso)
        return usuario

    @staticmethod
    def autenticar_usuario(usuario, contrasenia):
        return UsuarioData.obtener_usuario_por_usuario_y_contrasenia(usuario, contrasenia)

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        return UsuarioData.obtener_usuario_por_id(usuario_id)

    @staticmethod
    def buscar_usuarios(query):
        return UsuarioData.buscar_usuarios(query)

    @staticmethod
    def obtener_todos_usuarios():
        # Obténer todos los usuarios desde la base de datos
        usuarios = UsuarioData.GetAll()
        return usuarios

    @staticmethod
    def obtener_dts():
        return UsuarioData.obtener_dts()

    @staticmethod
    def obtener_asistentes():
        return UsuarioData.obtener_asistentes()

    @staticmethod
    def obtener_jugadores():
        return UsuarioData.obtener_jugadores()

    @staticmethod
    def obtener_tipo_usuario_controller(id_usuario):
        return UsuarioData.obtener_tipo_usuario_db(id_usuario)


class EquipoController:
    @staticmethod
    def crear_equipo_con_miembros(data):
        try:
            # Registrar los datos recibidos
            logger.info(f"Datos recibidos: {data}")

            # Crear el equipo
            equipo = Equipo(
                logo=data.get('logo'),
                nombre=data.get('nombre'),
                direccion=data.get('direccion'),
                ciudad=data.get('ciudad'),
                provincia=data.get('provincia'),
                cant_victorias_local=data.get('cant_victorias_local'),
                cant_victorias_visit=data.get('cant_victorias_visit'),
                campeonatos=data.get('campeonatos'),
                campeones_actuales=data.get('campeones_actuales')
            )
            equipo_guardado = EquipoData.crear_equipo(equipo)

            # Crear el DT
            dt_data = data.get('dt')
            try:
                dt = DT.objects.get(id=dt_data.get('id'))
                EquipoDtData.crear_equipodt(equipo_guardado, dt, convertir_fecha(dt_data.get('fecha_desde')),
                                            convertir_fecha(dt_data.get('fecha_hasta')))
            except DT.DoesNotExist:
                logger.error(f"DT con id {dt_data.get('id')} no existe.")
                raise

            # Crear asistentes
            asistentes_data = data.get('asistentes', [])
            for asistente_data in asistentes_data:
                try:
                    asistente = Asistente.objects.get(id=asistente_data.get('id'))
                    EquipoAsistenteData.crear_equipo_asistente(equipo_guardado, asistente,
                                                               convertir_fecha(asistente_data.get('fecha_desde')),
                                                               convertir_fecha(asistente_data.get('fecha_hasta')))
                except Asistente.DoesNotExist:
                    logger.error(f"Asistente con id {asistente_data.get('id')} no existe.")
                    raise

            # Crear jugadores
            jugadores_data = data.get('jugadores', [])
            for jugador_data in jugadores_data:
                try:
                    jugador = Jugador.objects.get(id=jugador_data.get('id'))
                    EquipoJugadorData.crear_equipo_jugador(equipo_guardado, jugador,
                                                           convertir_fecha(jugador_data.get('fecha_ingreso')),
                                                           convertir_fecha(jugador_data.get('fecha_salida')),
                                                           jugador_data.get('nro_jugador'),
                                                           jugador_data.get('posicion_pcpal'),
                                                           jugador_data.get('posicion_secundaria'))
                except Jugador.DoesNotExist:
                    logger.error(f"Jugador con id {jugador_data.get('id')} no existe.")
                    raise

            return equipo
        except Exception as e:
            logger.error(f"Error al crear el equipo y miembros: {e}")
            raise

    @staticmethod
    def fetch_all_equipos():
        return EquipoData.get_all_equipos()

    @staticmethod
    def fetch_equipo_by_id(equipo_id):
        return EquipoData.get_equipo_by_id(equipo_id)


class LigaController:
    @staticmethod
    def crear_liga(categoria, ptos_x_victoria, ptos_x_32_vict, ptos_x_32_derrota):
        return LigaData.crear_liga(categoria, ptos_x_victoria, ptos_x_32_vict, ptos_x_32_derrota)

    @staticmethod
    def obtener_todas_las_ligas():
        return LigaData.obtener_todas_las_ligas()

    @staticmethod
    def obtener_liga_por_id(liga_id):
        return LigaData.obtener_liga_por_id(liga_id)

class TemporadaController:

    @staticmethod
    def obtener_temporadas_por_liga(id_liga):
        return TemporadaData.obtener_temporadas_por_liga(id_liga)

    @staticmethod
    def crear_temporada(anio_desde, anio_hasta, estado, id_liga):
        liga = LigaData.obtener_liga_por_id(id_liga)
        return TemporadaData.crear_temporada(anio_desde, anio_hasta, estado, liga)

    @staticmethod
    def obtener_temporada(id):
        return TemporadaData.obtener_temporada_por_id(id)


class PosicionesController:
    @staticmethod
    def agregar_equipo(id_equipo, id_temporada):
        equipo = EquipoData.get_equipo_by_id(id_equipo)
        temporada = TemporadaData.obtener_temporada_por_id(id_temporada)
        return PosicionesData.agregar_equipo_a_temporada(equipo, temporada)

    @staticmethod
    def obtener_posiciones(id_temporada):
        return PosicionesData.obtener_posiciones_por_temporada(id_temporada)


class PartidoController:
    @staticmethod
    def agregar_partido(partido_data):

        return PartidoData.agregar_partido(partido_data)

    @staticmethod
    def obtener_partidos_por_temporada(temporada_id):
        return PartidoData.obtener_partidos_por_temporada(temporada_id)

    def ver_detalles_partido(id_partido):
        partido, sets = PartidoData.obtener_detalles_partido(id_partido)
        if partido and sets:
            return {
                "partido": {
                    "id": partido.id,
                    "fecha": partido.fecha,
                    "hora": partido.hora,
                    "local": partido.id_local.nombre,
                    "visita": partido.id_visita.nombre,
                    "set_ganados_local": partido.set_ganados_local,
                    "set_ganados_visita": partido.set_ganados_visita,
                    "id_temporada": partido.id_temporada.id,
                    "id_local": partido.id_local.id,
                    "id_visita": partido.id_visita.id
                },
                "sets": [{
                    "nro_set": s.nro_set,
                    "puntos_local": s.puntos_local,
                    "puntos_visita": s.puntos_visita
                } for s in sets]
            }
        return None

    def terminar_partido(id_partido):
        resultado = PartidoData.terminar_partido(id_partido)
        return resultado


class FormacionController:

    @staticmethod
    def crear_formacion(data):
        # Validar que el equipo exista
        e = EquipoData.get_equipo_by_id(data['id_equipo'])

        # Extraer los jugadores del array
        jugadores = data['jugadores']
        j1 = JugadorData.obtener_jugador_por_id(jugadores[0])
        j2 = JugadorData.obtener_jugador_por_id(jugadores[1])
        j3 = JugadorData.obtener_jugador_por_id(jugadores[2])
        j4 = JugadorData.obtener_jugador_por_id(jugadores[3])
        j5 = JugadorData.obtener_jugador_por_id(jugadores[4])
        j6 = JugadorData.obtener_jugador_por_id(jugadores[5])

        # Extraer el líbero
        l = JugadorData.obtener_jugador_por_id(data['libero'])

        # Crear la formación en la base de datos
        formacion = FormacionData.crear_formacion(e, j1, j2, j3, j4, j5, j6, l)
        return formacion

    @staticmethod
    def obtener_formacion_por_id(formacion_id):
        return FormacionData.obtener_formacion_por_id(formacion_id)

    @staticmethod
    def obtener_formaciones_por_equipo(id_equipo):
        return FormacionData.obtener_formaciones_por_equipo(id_equipo)

    def obtener_formaciones_equipo(id_equipo):
        return FormacionData.obtener_formaciones_equipo(id_equipo)


class EquipoJugadorController:
    @staticmethod
    def obtener_jugadores_por_equipo(equipo_id):
        return EquipoJugadorData.obtener_jugadores_por_equipo(equipo_id)


class SetController:
    @staticmethod
    def crear_set_controller(id_partido, puntos_local, puntos_visita, nro_set, id_formacion_local, id_formacion_visit):

        partido = PartidoData.obtener_partido_por_id(id_partido)
        local = FormacionData.obtener_formacion_por_id(id_formacion_local)
        visita = FormacionData.obtener_formacion_por_id(id_formacion_visit)

        set_data = {
            'id_partido': partido,
            'puntos_local': puntos_local,
            'puntos_visita': puntos_visita,
            'nro_set': nro_set,
            'id_formacion_local': local,
            'id_formacion_visit': visita
        }

        SetData.crear_set(set_data)

        if puntos_local > puntos_visita:
            partido.set_ganados_local += 1
        elif puntos_visita > puntos_local:
            partido.set_ganados_visita += 1

        PartidoData.actualizar_partido(partido)
        return {'success': True, 'partido': partido}

    @staticmethod
    def agregar_set(id_partido, puntos_local, puntos_visita, id_formacion_local, id_formacion_visit):

        nuevo_set = SetData.agregar_set(PartidoData.obtener_partido_por_id(id_partido),
                                        puntos_local, puntos_visita,
                                        FormacionData.obtener_formacion_por_id(id_formacion_local),
                                        FormacionData.obtener_formacion_por_id(id_formacion_visit))
        if nuevo_set:
            return {
                "id": nuevo_set.id,
                "nro_set": nuevo_set.nro_set,
                "puntos_local": nuevo_set.puntos_local,
                "puntos_visita": nuevo_set.puntos_visita
            }
        return None

    @staticmethod
    def obtener_sets_por_partido(id_partido):
        return SetData.obtener_sets_por_partido(id_partido)


class CambioController:
    @staticmethod
    def registrar_cambio(id_jugador_sale, id_jugador_entra, id_formacion, cerro, permanente):

        cambio = CambioData.guardar_cambio(JugadorData.obtener_jugador_por_id(id_jugador_sale),
                                           JugadorData.obtener_jugador_por_id(id_jugador_entra),
                                           FormacionData.obtener_formacion_por_id(id_formacion), cerro,
                                           permanente)

        # Preparar la respuesta
        response_data = {
            "id": cambio.id,
            "id_jugador_sale": cambio.id_jugador_sale.id,
            "id_jugador_entra": cambio.id_jugador_entra.id,
            "id_formacion": cambio.id_formacion.id,
            "cerro": cambio.cerro,
            "permanente": cambio.permanente
        }
        return response_data


class EstadisticasController:
    @staticmethod
    def registrar_estadisticas_controller(data):
        # Agregar validaciones adicionales si es necesario
        try:
            data['fecha_carga'] = datetime.now().date()
            if data['id_partido'] != 0:
                partido = Partido.objects.get(id=data['id_partido'])
            else:
                partido = None
            asistente = Asistente.objects.get(id_usuario=data['id_asistente'])
            jugador = Jugador.objects.get(id_usuario=data['id_jugador'])

            data['id_partido'] = partido
            data['id_asistente'] = asistente
            data['id_jugador'] = jugador

            estadistica = EstadisticasData.crear_estadisticas(data)
            return estadistica
        except Partido.DoesNotExist:
            raise ValueError('Partido no encontrado')
        except Asistente.DoesNotExist:
            raise ValueError('Asistente no encontrado')
        except Jugador.DoesNotExist:
            raise ValueError('Jugador no encontrado')

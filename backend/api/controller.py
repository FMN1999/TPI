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
from .db import *
from datetime import datetime
import logging
import bcrypt

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
        if usuario_obj and bcrypt.checkpw   (contrasenia.encode('utf-8'), usuario_obj.contrasenia.encode('utf-8')):
            return usuario_obj
        return None

    @staticmethod
    def registrar_usuario(data):
        contrasenia_plana = data.get('contrasenia')
        contrasenia_hashed = bcrypt.hashpw(contrasenia_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = Usuario(
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            ciudad_nacimiento=data.get('ciudad_nacimiento'),
            provincia_nacimiento=data.get('provincia_nacimiento'),
            email=data.get('email'),
            usuario=data.get('usuario'),
            contrasenia=contrasenia_hashed,  # Guardar la contraseña hasheada
            sexo=data.get('sexo')
        )
        usuario = UsuarioData.crear_usuario(user)
        tipo_usuario = data.get('tipo_usuario')
        if tipo_usuario == 'Asistente':
            asistente = Asistente(id_usuario=usuario)
            UsuarioData.crear_asistente(asistente)
        elif tipo_usuario == 'DT':
            dt = DT(telefono=data.get('telefono'), id_usuario=usuario)
            UsuarioData.crear_dt(dt)
        elif tipo_usuario == 'Jugador':
            jugador = Jugador(
                altura=data.get('altura'),
                peso=data.get('peso'),
                id_usuario=usuario
            )
            UsuarioData.crear_jugador(jugador)
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
        return UsuarioData.obtener_todos()

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
    def obtener_tipo_usuario(id_usuario):
        if UsuarioData.existe_asistente(id_usuario):
            return 'A'
        elif UsuarioData.existe_jugador(id_usuario):
            return 'J'
        elif UsuarioData.existe_dt(id_usuario):
            return 'D'
        else:
            return 'N'  # Ninguno de los anteriores"""


class EquipoController:
    @staticmethod
    def crear_equipo_con_miembros(data):
        try:
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

            dt_data = data.get('dt')
            dt = UsuarioData.obtener_dt_por_id(dt_data.get('id'))
            eqp_dt = EquipoDt(
                id_equipo=equipo_guardado,
                id_dt=dt,
                fecha_desde=convertir_fecha(dt_data.get('fecha_desde')),
                fecha_hasta=convertir_fecha(dt_data.get('fecha_hasta'))
            )
            EquipoDtData.crear_equipodt(eqp_dt)

            asistentes_data = data.get('asistentes', [])
            for asistente_data in asistentes_data:
                asistente = UsuarioData.obtener_asist_por_id(asistente_data.get('id'))
                eqp_asist = EquipoAsistente(
                    id_equipo=equipo_guardado,
                    id_asistente=asistente,
                    fecha_desde=convertir_fecha(asistente_data.get('fecha_desde')),
                    decha_hasta=convertir_fecha(asistente_data.get('fecha_hasta'))
                )
                EquipoAsistenteData.crear_equipo_asistente(eqp_asist)

            jugadores_data = data.get('jugadores', [])
            for jugador_data in jugadores_data:
                jugador = UsuarioData.obtener_jug_por_id(jugador_data.get('id'))
                eqp_jug = EquipoJugador(
                    id_equipo=equipo_guardado,
                    id_jugador=jugador,
                    fecha_ingreso=convertir_fecha(jugador_data.get('fecha_ingreso')),
                    fecha_salida=convertir_fecha(jugador_data.get('fecha_salida')),
                    nro_jugador=jugador_data.get('nro_jugador'),
                    posicion_pcpal=jugador_data.get('posicion_pcpal'),
                    posicion_secundaria=jugador_data.get('posicion_secundaria')
                )
                EquipoJugadorData.crear_equipo_jugador(eqp_jug)

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
    def crear_liga(data):
        liga = Liga(
            categoria=data.get('categoria'),
            ptos_x_victoria=data.get('ptos_x_victoria'),
            ptos_x_32_vict=data.get('ptos_x_32_vict'),
            ptos_x_32_derrota=data.get('ptos_x_32_derrota')
        )
        return LigaData.crear_liga(liga)

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
    def crear_temporada(data):
        liga = LigaData.obtener_liga_por_id(data.get('id_liga'))
        temp = Temporada(
            anio_desde=data.get('anio_desde'),
            anio_hasta=data.get('anio_hasta'),
            estado=data.get('estado'),
            id_liga=liga
        )
        return TemporadaData.crear_temporada(temp)

    @staticmethod
    def obtener_temporada(id):
        return TemporadaData.obtener_temporada_por_id(id)


class PosicionesController:
    @staticmethod
    def agregar_equipo(id_equipo, id_temporada):
        equipo = EquipoData.get_equipo_by_id(id_equipo)
        temporada = TemporadaData.obtener_temporada_por_id(id_temporada)
        pos = Posiciones(
            id_equipo=equipo,
            id_temporada=temporada,
            puntaje=0,
            set_ganados=0,
            set_en_contra=0,
            diferencia_sets=0
        )
        return PosicionesData.agregar_equipo_a_temporada(pos)

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

    @staticmethod
    def ver_detalles_partido(id_partido):
        partido = PartidoData.obtener_partido_por_id(id_partido)
        sets = SetData.obtener_sets_por_partido(partido)
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

    @staticmethod
    def terminar_partido(id_partido):
        try:
            partido = PartidoData.obtener_partido_por_id(id_partido)
            temporada = TemporadaData.obtener_temporada_por_id(partido.id_temporada.id)
            liga = LigaData.obtener_liga_por_id(temporada.id_liga.id)
            puntos_local = 0
            puntos_visita = 0

            # Calcular puntos para el local
            if partido.set_ganados_local >= 3:
                if partido.set_ganados_visita <= 1:
                    puntos_local = liga.ptos_x_victoria
                elif partido.set_ganados_visita == 2:
                    puntos_local = liga.ptos_x_32_vict
            else:
                puntos_local = liga.ptos_x_32_derrota if partido.set_ganados_local == 2 else 0

            # Calcular puntos para el visitante
            if partido.set_ganados_visita >= 3:
                if partido.set_ganados_local <= 1:
                    puntos_visita = liga.ptos_x_victoria
                elif partido.set_ganados_local == 2:
                    puntos_visita = liga.ptos_x_32_vict
            else:
                puntos_visita = liga.ptos_x_32_derrota if partido.set_ganados_visita == 2 else 0

            pos_loc = PosicionesData.obtener_por_equipo_temp(partido.id_local, temporada)
            pos_loc.puntaje += puntos_local
            pos_loc.set_ganados += partido.sets_ganados_local
            pos_loc.set_en_contra += partido.sets_ganados_visita
            pos_loc.diferencia_sets = pos_loc.set_ganados - pos_loc.set_en_contra
            PosicionesData.actualizar_posicion(pos_loc)

            pos_vis = PosicionesData.obtener_por_equipo_temp(partido.id_visit, temporada)
            pos_vis.puntaje += puntos_visita
            pos_vis.set_ganados += partido.sets_ganados_visita
            pos_vis.set_en_contra += partido.sets_ganados_local
            pos_vis.diferencia_sets = pos_vis.set_ganados - pos_vis.set_en_contra
            PosicionesData.actualizar_posicion(pos_vis)
            return True
        except:
            return False


class FormacionController:
    @staticmethod
    def crear_formacion(data):
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

        formacion = Formacion(
            jugador_1=j1,
            jugador_2=j2,
            jugador_3=j3,
            jugador_4=j4,
            jugador_5=j5,
            jugador_6=j6,
            libero=l
        )
        # Crear la formación en la base de datos
        return FormacionData.crear_formacion(formacion)

    @staticmethod
    def obtener_formacion_por_id(formacion_id):
        return FormacionData.obtener_formacion_por_id(formacion_id)

    @staticmethod
    def obtener_formaciones_por_equipo(id_equipo):
        return FormacionData.obtener_formaciones_por_equipo(id_equipo)

    @staticmethod
    def obtener_formaciones_equipo(id_equipo):
        return FormacionData.obtener_formaciones_equipo(id_equipo)


class EquipoJugadorController:
    @staticmethod
    def obtener_jugadores_por_equipo(equipo_id):
        return EquipoJugadorData.obtener_jugadores_por_equipo(equipo_id)


class SetController:
    @staticmethod
    def crear_set_controller(data):
        partido = PartidoData.obtener_partido_por_id(data.get('id_partido'))
        set_data = Set(
            id_partido=partido,
            puntos_local=data.get('puntos_local'),
            puntos_visita=data.get('puntos_visita'),
            nro_set=data.get('nro_set'),
            id_formacion_local=FormacionData.obtener_formacion_por_id(data.get('id_formacion_local')),
            id_formacion_visit=FormacionData.obtener_formacion_por_id(data.get('id_formacion_visit'))
        )

        SetData.crear_set(set_data)

        if set_data.puntos_local > set_data.puntos_visita:
            partido.set_ganados_local += 1
        elif set_data.puntos_visita > set_data.puntos_local:
            partido.set_ganados_visita += 1

        PartidoData.actualizar_partido(partido)
        return {'success': True, 'partido': partido}

    @staticmethod
    def agregar_set(data):
        nro_sets = SetData.cuenta_sets(data.get('id_partido'))
        partido = PartidoData.obtener_partido_por_id(data.get('id_partido'))
        nuevo_set = Set(
            id_partido=partido,
            puntos_local=data.get('puntos_local'),
            puntos_visita=data.get('puntos_visita'),
            nro_set=nro_sets,
            id_formacion_local = FormacionData.obtener_formacion_por_id(data.get('id_formacion_local')),
            id_formacion_visit=FormacionData.obtener_formacion_por_id(data.get('id_formacion_visit'))
        )
        SetData.agregar_set(nuevo_set)

        if nuevo_set.puntos_local > nuevo_set.puntos_visita:
            partido.set_ganados_local += 1
        else:
            partido.set_ganados_visita += 1
        PartidoData.actualizar_partido(partido)

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
    def registrar_cambio(data):

        cambio = Cambio(
            id_jugador_sale=JugadorData.obtener_jugador_por_id(int(data['id_jugador_sale'])),
            id_jugador_entra=JugadorData.obtener_jugador_por_id(int(data['id_jugador_entra'])),
            id_formacion=FormacionData.obtener_formacion_por_id(int(data['id_formacion'])),
            cerro=data.get('cerro', False),
            permanente=data.get('permanente', False)
        )

        CambioData.guardar_cambio(cambio)

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
                partido = PartidoData.obtener_partido_por_id(data['id_partido'])
            else:
                partido = None
            asistente = UsuarioData.obtener_asist_por_id(data['id_asistente'])
            jugador = UsuarioData.obtener_jug_por_id(data['id_jugador'])

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

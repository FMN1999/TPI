from .models import *


class UsuarioData:
    @staticmethod
    def obtener_usuario_por_usuario(usuario):
        try:
            return Usuario.objects.get(usuario=usuario)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def crear_usuario(data: Usuario):
        data.save()
        return data

    @staticmethod
    def crear_asistente(asist: Asistente):
        asist.save()
        return asist

    @staticmethod
    def crear_dt(dt: DT):
        dt.save()
        return dt

    @staticmethod
    def crear_jugador(jugador: Jugador):
        jugador.save()
        return jugador

    @staticmethod
    def obtener_usuario_por_usuario_y_contrasenia(usuario, contrasenia):
        try:
            return Usuario.objects.get(usuario=usuario, contrasenia=contrasenia)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def buscar_usuarios(query):
        return Usuario.objects.filter(nombre__icontains=query) | Usuario.objects.filter(apellido__icontains=query)

    @classmethod
    def obtener_todos(cls):
        usuarios = Usuario.objects.all()
        return usuarios

    @staticmethod
    def obtener_dts():
        return DT.objects.all()

    @staticmethod
    def obtener_asistentes():
        return Asistente.objects.all()

    @staticmethod
    def obtener_jugadores():
        return Jugador.objects.all()

    @staticmethod
    def existe_asistente(id_usuario):
        return Asistente.objects.filter(id_usuario=id_usuario).exists()

    @staticmethod
    def existe_jugador(id_usuario):
        return Jugador.objects.filter(id_usuario=id_usuario).exists()

    @staticmethod
    def existe_dt(id_usuario):
        return DT.objects.filter(id_usuario=id_usuario).exists()

    @staticmethod
    def obtener_dt_por_id(id_dt):
        return DT.objects.get(id_usuario=id_dt)

    @staticmethod
    def obtener_asist_por_id(id_asist):
        return Asistente.objects.get(id_usuario=id_asist)

    @staticmethod
    def obtener_jug_por_id(id_jug):
        return Jugador.objects.get(id_usuario=id_jug)


class EquipoData:
    @staticmethod
    def crear_equipo(equipo):
        equipo.save()
        return equipo

    @staticmethod
    def get_all_equipos():
        return Equipo.objects.all()

    @staticmethod
    def get_equipo_by_id(equipo_id):
        try:
            return Equipo.objects.get(id=equipo_id)
        except Equipo.DoesNotExist:
            return None


class EquipoAsistenteData:
    @staticmethod
    def crear_equipo_asistente(equipo_asistente: EquipoAsistente):
        equipo_asistente.save()
        return equipo_asistente


class EquipoDtData:
    @staticmethod
    def crear_equipodt(equipo_dt: EquipoDt):
        equipo_dt.save()
        return equipo_dt


class EquipoJugadorData:
    @staticmethod
    def crear_equipo_jugador(equipo_jugador: EquipoJugador):
        equipo_jugador.save()
        return equipo_jugador

    @staticmethod
    def obtener_jugadores_por_equipo(equipo_id):
        return EquipoJugador.objects.filter(id_equipo=equipo_id).all()


class LigaData:
    @staticmethod
    def crear_liga(liga: Liga):
        liga.save()
        return liga

    @staticmethod
    def obtener_todas_las_ligas():
        return Liga.objects.all()

    @staticmethod
    def obtener_liga_por_id(liga_id):
        return Liga.objects.get(id=liga_id)


class TemporadaData:
    @staticmethod
    def obtener_temporadas_por_liga(id_liga):
        return Temporada.objects.filter(id_liga=id_liga).all()

    @staticmethod
    def crear_temporada(nueva_temporada: Temporada):
        nueva_temporada.save()
        return nueva_temporada

    @staticmethod
    def obtener_temporada_por_id(id):
        return Temporada.objects.get(id=id)


class PosicionesData:
    @staticmethod
    def agregar_equipo_a_temporada(nueva_posicion: Posiciones):
        nueva_posicion.save()
        return nueva_posicion

    @staticmethod
    def obtener_posiciones_por_temporada(id_temporada):
        return Posiciones.objects.filter(id_temporada=id_temporada)

    @staticmethod
    def actualizar_posicion(posicion: Posiciones):
        try:
            posicion.save()
            return True
        except:
            return False

    @staticmethod
    def obtener_por_equipo_temp(equipo, temporada):
        return Posiciones.objects.filter(id_quipo=equipo, id_temporada=temporada)


class PartidoData:
    @staticmethod
    def agregar_partido(partido: Partido):
        partido.save()
        return partido

    @staticmethod
    def obtener_partidos_por_temporada(temporada_id):
        return Partido.objects.filter(id_temporada=temporada_id)

    @staticmethod
    def obtener_partido_por_id(partido_id):
        return Partido.objects.get(id=partido_id)

    @staticmethod
    def actualizar_partido(partido):
        partido.save()


class FormacionData:
    @staticmethod
    def crear_formacion(formacion: Formacion):
        try:
            formacion.save()
            return formacion
        except Exception as e:
            print(f"Error al crear la formación: {e}")
            raise

    @staticmethod
    def obtener_formacion_por_id(id):
        return Formacion.objects.get(id=id)

    @staticmethod
    def obtener_formaciones_por_equipo(equipo_id):
        return Formacion.objects.get(id_equipo=equipo_id)

    @staticmethod
    def obtener_formaciones_equipo(id_equipo):
        try:
            return Formacion.objects.filter(id_equipo=id_equipo)
        except:
            return None


class JugadorData:
    @staticmethod
    def obtener_jugador_por_id(jugador_id):
        return Jugador.objects.get(id=jugador_id)


class SetData:
    @staticmethod
    def crear_set(set: Set):
        set.save()
        return set

    @staticmethod
    def cuenta_sets(id_p):
        return Set.objects.filter(id_partido=id_p).count() + 1

    @staticmethod
    def agregar_set(set: Set):
        try:
            set.save()
            return set
        except :
            return None

    @staticmethod
    def obtener_sets_por_partido(id_partido):
        try:
            return Set.objects.filter(id_partido=id_partido)
        except:
            return None


class CambioData:
    @staticmethod
    def guardar_cambio(cambio: Cambio):
        cambio.save()
        return cambio


class EstadisticasData:
    @staticmethod
    def crear_estadisticas(estadistica: Estadisticas):
        estadistica.save()
        return estadistica

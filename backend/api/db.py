from .models import *

class UsuarioData:
    @staticmethod
    def obtener_usuario_por_usuario(usuario):
        try:
            return Usuario.objects.get(usuario=usuario)
        except Usuario.DoesNotExist:
            return None

    def crear_usuario(data):
        usuario = Usuario(
            fecha_nacimiento=data.get('fecha_nacimiento'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            ciudad_nacimiento=data.get('ciudad_nacimiento'),
            provincia_nacimiento=data.get('provincia_nacimiento'),
            email=data.get('email'),
            usuario=data.get('usuario'),
            contrasenia=data.get('contrasenia'),
            sexo=data.get('sexo')
        )
        usuario.save()
        return usuario

    @staticmethod
    def crear_asistente(usuario):
        asistente = Asistente(id_usuario=usuario)
        asistente.save()
        return asistente

    @staticmethod
    def crear_dt(usuario, telefono):
        dt = DT(id_usuario=usuario, telefono=telefono)
        dt.save()
        return dt

    @staticmethod
    def crear_jugador(usuario, altura, peso):
        jugador = Jugador(id_usuario=usuario, altura=altura, peso=peso)
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
    def GetAll(cls):
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
        return Jugador.objects  .all()


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
    def crear_equipo_asistente(equipo, asistente, fecha_desde, fecha_hasta):
        equipo_asistente = EquipoAsistente(
            id_equipo=equipo,
            id_asistente=asistente,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        equipo_asistente.save()


class EquipoDtData:
    @staticmethod
    def crear_equipodt(equipo, dt, fecha_desde, fecha_hasta):
        equipo_dt = EquipoDt(
            id_equipo=equipo,
            id_dt=dt,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        equipo_dt.save()


class EquipoJugadorData:
    @staticmethod
    def crear_equipo_jugador(equipo, jugador, ingreso, salida, nro, pos_pcpal, pos_secun):
        equipo_jugador = EquipoJugador(
            id_equipo=equipo,
            id_jugador=jugador,
            fecha_ingreso=ingreso,
            fecha_salida=salida,
            nro_jugador=nro,
            posicion_pcpal=pos_pcpal,
            posicion_secundaria=pos_secun,
        )
        equipo_jugador.save()


class LigaData:
    @staticmethod
    def crear_liga(categoria, ptos_x_victoria, ptos_x_32_vict, ptos_x_32_derrota):
        liga = Liga(
            categoria=categoria,
            ptos_x_victoria=ptos_x_victoria,
            ptos_x_32_vict=ptos_x_32_vict,
            ptos_x_32_derrota=ptos_x_32_derrota
        )
        liga.save()
        return liga

    @staticmethod
    def obtener_todas_las_ligas():
        return Liga.objects.all()

    @staticmethod
    def obtener_liga_por_id(liga_id):
        return Liga.objects.filter(id=liga_id).first()


class TemporadaData:
    @staticmethod
    def obtener_temporadas_por_liga(id_liga):
        return Temporada.objects.filter(id_liga=id_liga).all()

    @staticmethod
    def crear_temporada(anio_desde, anio_hasta, estado, id_liga):
        nueva_temporada = Temporada(anio_desde=anio_desde, anio_hasta=anio_hasta, estado=estado, id_liga=id_liga)
        nueva_temporada.save()
        return nueva_temporada

    def obtener_temporada_por_id(id):
        return Temporada.objects.get(id=id)


class PosicionesData:
    @staticmethod
    def agregar_equipo_a_temporada(id_equipo, id_temporada):
        nueva_posicion = Posiciones(id_equipo=id_equipo, id_temporada=id_temporada, puntaje=0, set_ganados=0,
                                    set_en_contra=0, diferencia_sets=0)
        nueva_posicion.save()
        return nueva_posicion

    @staticmethod
    def obtener_posiciones_por_temporada(id_temporada):
        return Posiciones.objects.filter(id_temporada=id_temporada)


class PartidoData:
    def agregar_partido(partido_data):
        partido = Partido(
            id_local=EquipoData.get_equipo_by_id(partido_data['id_local']),
            id_visita=EquipoData.get_equipo_by_id(partido_data['id_visita']),
            fecha=partido_data['fecha'],
            hora=partido_data['hora'],
            set_ganados_local=partido_data.get('set_ganados_local', 0),
            set_ganados_visita=partido_data.get('set_ganados_visita', 0),
            id_temporada=TemporadaData.obtener_temporada_por_id(partido_data['id_temporada'])
        )
        partido.save()
        return partido


    @staticmethod
    def obtener_partidos_por_temporada(temporada_id):
        return Partido.objects.filter(id_temporada=temporada_id)
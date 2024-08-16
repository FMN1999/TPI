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
        return Jugador.objects.all()

    @staticmethod
    def obtener_tipo_usuario_db(id_usuario):
        if Asistente.objects.filter(id_usuario=id_usuario).exists():
            return 'A'
        elif Jugador.objects.filter(id_usuario=id_usuario).exists():
            return 'J'
        elif DT.objects.filter(id_usuario=id_usuario).exists():
            return 'D'
        else:
            return 'N'  # Ninguno de los anteriores


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

    @staticmethod
    def obtener_jugadores_por_equipo(equipo_id):
        return EquipoJugador.objects.filter(id_equipo=equipo_id).all()


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

    def actualizar_posicion(id_equipo, id_temporada, puntos, sets_ganados, sets_en_contra):
        try:
            posicion, created = Posiciones.objects.get_or_create(
                id_equipo=id_equipo,
                id_temporada=id_temporada,
                defaults={'puntaje': 0, 'set_ganados': 0, 'set_en_contra': 0, 'diferencia_sets': 0}
            )
            posicion.puntaje += puntos
            posicion.set_ganados += sets_ganados
            posicion.set_en_contra += sets_en_contra
            posicion.diferencia_sets = posicion.set_ganados - posicion.set_en_contra
            posicion.save()
            return True
        except Exception as e:
            return False


class PartidoData:
    @staticmethod
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

    @staticmethod
    def obtener_partido_por_id(partido_id):
        return Partido.objects.get(id=partido_id)

    @staticmethod
    def actualizar_partido(partido):
        partido.save()

    @staticmethod
    def obtener_detalles_partido(id_partido):
        try:
            partido = Partido.objects.get(id=id_partido)
            sets = Set.objects.filter(id_partido=id_partido).order_by('nro_set')
            return partido, sets
        except Partido.DoesNotExist:
            return None, None

    @staticmethod
    def terminar_partido(id_partido):
        try:
            partido = Partido.objects.get(id=id_partido)
            temporada = Temporada.objects.get(id=partido.id_temporada.id)
            liga = Liga.objects.get(id=temporada.id_liga.id)

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

            PosicionesData.actualizar_posicion(partido.id_local.id, temporada.id, puntos_local, partido.set_ganados_local,
                                partido.set_ganados_visita)
            PosicionesData.actualizar_posicion(partido.id_visita.id, temporada.id, puntos_visita, partido.set_ganados_visita,
                                partido.set_ganados_local)
            return True
        except Exception as e:
            return False


class FormacionData:
    def crear_formacion(e, j1, j2, j3, j4,j5, j6, l):
        try:
            formacion = Formacion(
                id_equipo=e,
                jugador_1=j1,
                jugador_2=j2,
                jugador_3=j3,
                jugador_4=j4,
                jugador_5=j5,
                jugador_6=j6,
                libero=l
            )
            formacion.save()
            return formacion
        except Exception as e:
            # Puedes registrar el error o hacer algo más con él
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
            formaciones = Formacion.objects.filter(id_equipo=id_equipo)
            return formaciones
        except Exception as e:
            print(f"Error al obtener formaciones para el equipo {id_equipo}: {e}")
            return None


class JugadorData:
    @staticmethod
    def obtener_jugador_por_id(jugador_id):
        return Jugador.objects.get(id=jugador_id)


class SetData:
    @staticmethod
    def crear_set(data):
        new_set = Set.objects.create(**data)
        return new_set

    @staticmethod
    def agregar_set(partido, puntos_local, puntos_visita, id_formacion_local, id_formacion_visit):
        try:

            nro_set = Set.objects.filter(id_partido=partido.id).count() + 1
            nuevo_set = Set(
                id_partido=partido,
                puntos_local=puntos_local,
                puntos_visita=puntos_visita,
                nro_set=nro_set,
                id_formacion_local=id_formacion_local,
                id_formacion_visit=id_formacion_visit
            )
            nuevo_set.save()
            print("Supuestamente guardado")
            if puntos_local > puntos_visita:
                partido.set_ganados_local += 1
            else:
                partido.set_ganados_visita += 1
            partido.save()
            return nuevo_set
        except Exception as e:
            return None

    def obtener_sets_por_partido(id_partido):
        try:
            sets = Set.objects.filter(id_partido=id_partido)
            return sets
        except Exception as e:
            print(f"Error al obtener sets para el partido {id_partido}: {e}")
            return None


class CambioData:
    @staticmethod
    def guardar_cambio(id_jugador_sale, id_jugador_entra, id_formacion, cerro=False, permanente=False):
        cambio = Cambio(
            id_jugador_sale=id_jugador_sale,
            id_jugador_entra=id_jugador_entra,
            id_formacion=id_formacion,
            cerro=cerro,
            permanente=permanente
        )
        cambio.save()
        return cambio
    
# db.py
class EstadisticasData:
    def crear_estadisticas(data):
        estadistica = Estadisticas.objects.create(
            remates_fallidos=data['remates_fallidos'],
            remates_buenos=data['remates_buenos'],
            defensas_fallidas=data['defensas_fallidas'],
            defensas_buenas=data['defensas_buenas'],
            bloqueos_fallidos=data['bloqueos_fallidos'],
            bloqueos_buenos=data['bloqueos_buenos'],
            saques_fallidos=data['saques_fallidos'],
            saques_buenos=data['saques_buenos'],
            recepciones_buenas=data['recepciones_buenas'],
            recepciones_fallidas=data['recepciones_fallidas'],
            fecha_carga=data['fecha_carga'],
            id_partido=data['id_partido'],
            id_asistente=data['id_asistente'],
            id_jugador=data['id_jugador'],
        )
        return estadistica

from datetime import date, time
from typing import Tuple, List, Any
from werkzeug.security import generate_password_hash, check_password_hash


class Asistente:
    def __int__(self, _id: int, id_usuario: int) -> None:
        self.id = _id
        self.idUsuario = id_usuario

    def lst(self) -> List[Any]:
        return [self.id, self.idUsuario]

    def __repr__(self):
        return f"Asistente({self.id, self.idUsuario})"


class Cambio:
    def __init__(self, _id: int, id_jugador_sale: int, id_jugador_entra: int, id_formacion: int, cerro: bool,
                 permanente: bool) -> None:
        self.id = _id
        self.idJugadorSale = id_jugador_sale
        self.idJugadorEntra = id_jugador_entra
        self.idFormacion = id_formacion
        self.cerro = cerro
        self.permanente = permanente

    def lst(self) -> List[Any]:
        return [self.id, self.idJugadorSale, self.idJugadorEntra, self.idFormacion, self.cerro, self.permanente]

    def __repr__(self):
        return f"Cambio({self.id, self.idJugadorSale, self.idJugadorEntra, self.idFormacion, self.cerro,
        self.permanente})"


class DT:
    def __int__(self, _id: int, id_usuario: int, telefono: str) -> None:
        self.id = _id
        self.idUsuario = id_usuario
        self.telefono = telefono

    def lst(self) -> List[Any]:
        return [self.id, self.idUsuario, self.telefono]

    def __repr__(self):
        return f"DT({self.id, self.idUsuario, self.telefono})"


class Equipo:
    def __int__(self, _id: int, nombre: str, logo: str, direccion: str, ciudad: str, provincia: str,
                cant_victorias_local: int, cant_derrotas_local: int, cant_victorias_visit: int,
                cant_derrotas_visit: int, campeonatos: int, campeones_actuales: bool) -> None:
        self.id = _id
        self.nombre = nombre
        self.logo = logo
        self.direccion = direccion
        self.ciudad = ciudad
        self.provincia = provincia
        self.cantVictoriasLocal = cant_victorias_local
        self.cantDerrotasLocal = cant_derrotas_local
        self.cantVictoriasVisita = cant_victorias_visit
        self.cantDerrotasVisita = cant_derrotas_visit
        self.campeonatos = campeonatos
        self.campeonesActuales = campeones_actuales

    def lst(self) -> List[Any]:
        return [self.id, self.nombre, self.logo, self.direccion, self.ciudad, self.provincia, self.cantVictoriasLocal,
                self.cantDerrotasLocal, self.cantVictoriasVisita, self.cantDerrotasVisita, self.campeonatos,
                self.campeonesActuales]

    def __repr__(self):
        return f"Equipo({self.id, self.nombre, self.logo, self.direccion, self.ciudad, self.provincia,
        self.cantVictoriasLocal, self.cantDerrotasLocal, self.cantVictoriasVisita,
        self.cantDerrotasVisita, self.campeonatos, self.campeonesActuales})"


class EquipoAsistente:
    def __int__(self, _id: int, id_equipo: int, id_asistente: int, fecha_desde: date, fecha_hasta: date) -> None:
        self.id = _id
        self.idEquipo = id_equipo
        self.idAsistente = id_asistente
        self.fechaDesde = fecha_desde
        self.fechaHasta = fecha_hasta

    def lst(self) -> List[Any]:
        return [self.id, self.idEquipo, self.idAsistente, self.fechaDesde, self.fechaHasta]

    def __repr__(self):
        return f"EquipoAsistente({self.id, self.idEquipo, self.idAsistente, self.fechaDesde, self.fechaHasta})"


class EquipoDt:
    def __int__(self, _id: int, id_equipo: int, id_dt: int, fecha_desde: date, fecha_hasta: date) -> None:
        self.id = _id
        self.idEquipo = id_equipo
        self.idDt = id_dt
        self.fechaDesde = fecha_desde
        self.fechaHasta = fecha_hasta

    def lst(self) -> List[Any]:
        return [self.id, self.idEquipo, self.idDt, self.fechaDesde, self.fechaHasta]

    def __repr__(self):
        return f"EquipoDt({self.id, self.idEquipo, self.idDt, self.fechaDesde, self.fechaHasta})"


class EquipoJugador:
    def __int__(self, _id: int, id_equipo: int, id_jugador: int, fecha_ingreso: date, fecha_salida: date,
                nro_jugador: int, posicion_pcpal: str, posicion_secundaria: str) -> None:
        self.id = _id
        self.idEquipo = id_equipo
        self.idJugador = id_jugador
        self.fechaIngreso = fecha_ingreso
        self.fechaSalida = fecha_salida
        self.nroJugador = nro_jugador
        self.posicionPcpal = posicion_pcpal
        self.posicionSecundaria = posicion_secundaria

    def lst(self) -> List[Any]:
        return [self.id, self.idEquipo, self.idJugador, self.fechaIngreso, self.fechaSalida, self.nroJugador,
                self.posicionPcpal, self.posicionSecundaria]

    def __repr__(self):
        return f"EquipoJugador({self.id, self.idEquipo, self.idJugador, self.fechaIngreso, self.fechaSalida,
        self.nroJugador, self.posicionPcpal, self.posicionSecundaria})"


class Estadisticas:
    def __init__(self, _id: int, remates_fallidos: int, remates_buenos: int, defensas_fallidas: int,
                 defensas_buenas: int, bloqueos_fallidos: int, bloqueos_buenos: int, saques_fallidos: int,
                 saques_buenos: int, recepciones_buenas: int, recepciones_fallidas: int, fecha_carga: date,
                 id_partido: int, id_asistente: int, id_jugador: int) -> None:
        self.id = _id
        self.rematesFallidos = remates_fallidos
        self.rematesBuenos = remates_buenos
        self.defensasFallidas = defensas_fallidas
        self.defensasBuenas = defensas_buenas
        self.bloqueosFallidos = bloqueos_fallidos
        self.bloqueosBuenos = bloqueos_buenos
        self.saquesFallidos = saques_fallidos
        self.saquesBuenos = saques_buenos
        self.recepcionesBuenas = recepciones_buenas
        self.recepcionesFallidas = recepciones_fallidas
        self.fechaCarga = fecha_carga
        self.idPartido = id_partido
        self.idAsistente = id_asistente
        self.idJugador = id_jugador


def lst(self) -> List[Any]:
    return [self.id, self.rematesFallidos, self.rematesBuenos, self.defensasFallidas, self.defensasBuenas,
            self.bloqueosFallidos, self.bloqueosBuenos, self.saquesFallidos, self.saquesBuenos, self.recepcionesBuenas,
            self.recepcionesFallidas, self.fechaCarga, self.idPartido, self.idAsistente, self.idJugador]


def __repr__(self):
    return f"Estadisticas({self.id, self.rematesFallidos, self.rematesBuenos, self.defensasFallidas, 
    self.defensasBuenas, self.bloqueosFallidos, self.bloqueosBuenos, self.saquesFallidos, self.saquesBuenos,
    self.recepcionesBuenas, self.recepcionesFallidas, self.fechaCarga, self.idPartido, self.idAsistente,
    self.idJugador})"


class Formacion:
    def __init__(self, _id: int, id_equipo: int, jugador_1:int, jugador_2: int, jugador_3: int, jugador_4: int,
                 jugador_5: int, jugador_6: int, libero: int) -> None:
        self.id = _id
        self.idEquipo = id_equipo
        self.jugador1 = jugador_1
        self.jugador2 = jugador_2
        self.jugador3 = jugador_3
        self.jugador4 = jugador_4
        self.jugador5 = jugador_5
        self.jugador6 = jugador_6
        self.libero = libero


    def lst(self) -> List[Any]:
        return [self.id, self.idEquipo, self.jugador1, self.jugador2, self.jugador3, self.jugador4, self.jugador5,
                self.jugador6, self.libero]


    def __repr__(self):
        return f"Formación({self.id, self.idEquipo, self.jugador1, self.jugador2, self.jugador3, self.jugador4, 
        self.jugador5, self.jugador6, self.libero})"


class Jugador:
    def __init__(self, _id: int, altura: float, peso: float, id_usuario: int) -> None:
        self.id = _id
        self.altura = altura
        self.peso = peso
        self.idUsuario = id_usuario

    def lst(self) -> List[Any]:
        return [self.id, self.altura, self.peso, self.idUsuario]

    def __repr__(self):
        return f"Jugador({self.id, self.altura, self.peso, self.idUsuario})"


class Liga:
    def __init__(self, _id: int, categoria: str, ptos_x_victoria: int, ptos_x32_vict: int,
                 ptos_x_32_derrota: int) -> None:
        self.id = _id
        self.categoria = categoria
        self.ptosVictoria = ptos_x_victoria
        self.ptos32Victoria = ptos_x32_vict
        self.ptos32Derrota = ptos_x_32_derrota

    def lst(self) -> List[Any]:
        return [self.id, self.categoria, self.ptosVictoria, self.ptos32Victoria, self.ptos32Derrota]

    def __repr__(self):
        return f"Liga({self.id, self.categoria, self.ptosVictoria, self.ptos32Victoria, self.ptos32Derrota})"


class Partido:
    def __init__(self, _id: int, id_local: int, fecha: date, hora: time, set_ganados_local: int, id_temporada: int,
                 set_ganados_visita: int, id_visita: int) -> None:
        self.id = _id
        self.idLocal = id_local
        self.fecha = fecha
        self.hora = hora
        self.setGanadosLocal = set_ganados_local
        self.idTemporada = id_temporada
        self.setGanadosVisita = set_ganados_visita
        self.idVisita = id_visita

    def lst(self) -> List[Any]:
        return [self.id, self.idLocal, self.fecha, self.hora, self.setGanadosLocal, self.idTemporada,
                self.setGanadosVisita, self.idVisita]

    def __repr__(self):
        return f"({self.id, self.idLocal, self.fecha, self.hora, self.setGanadosLocal, self.idTemporada, 
        self.setGanadosVisita, self.idVisita})"


class Posiciones:
    def __init__(self, _id: int, id_equipo: int, id_temporada: int, puntaje: int, set_ganados: int, set_en_contra: int,
                 diferencia_sets: int) -> None:
        self.id = _id
        self.idEquipo = id_equipo
        self.idTemporada = id_temporada
        self.puntaje = puntaje
        self.setGanados = set_ganados
        self.setContra = set_en_contra
        self.diferenciaSets = diferencia_sets

    def lst(self) -> List[Any]:
        return [self.id, self.idEquipo, self.idTemporada, self.puntaje, self.setGanados, self.setContra,
                self.diferenciaSets]

    def __repr__(self):
        return f"({self.id, self.idEquipo, self.idTemporada, self.puntaje, self.setGanados, self.setContra, 
        self.diferenciaSets})"


class Set:
    def __init__(self, _id: int, puntos_visita: int, puntos_local: int, id_partido: int, nro_set: int,
                 id_formacion_local: int, id_formacion_visit: int) -> None:
        self.id = _id
        self.puntosVisita = puntos_visita
        self.puntosLocal = puntos_local
        self.idPartido = id_partido
        self.nroSet = nro_set
        self.idFormacionLocal = id_formacion_local
        self.idFormacionVisita = id_formacion_visit

    def lst(self) -> List[Any]:
        return [self.id, self.puntosVisita, self.puntosLocal, self.idPartido, self.nroSet, self.idFormacionLocal,
                self.idFormacionVisita]

    def __repr__(self):
        return f"({self.id, self.puntosVisita, self.puntosLocal, self.idPartido, self.nroSet, self.idFormacionLocal, 
        self.idFormacionVisita})"


class Temporada:
    def __init__(self, _id: int, anio_desde: int, anio_hasta: int, estado: str, id_liga: int) -> None:
        self.id = _id
        self.anioDesde = anio_desde
        self.anioHasta = anio_hasta
        self.estado = estado
        self.idLiga = id_liga

    def lst(self) -> List[Any]:
        return [self.id, self.anioDesde, self.anioHasta, self.estado, self.idLiga]

    def __repr__(self):
        return f"({self.id, self.anioDesde, self.anioHasta, self.estado, self.idLiga})"


class Usuario:
    def __init__(self, _id: int, usuario: str, contrasenia: str, fecha_nacimiento: date, nombre: str, apellido: str,
                 ciudad_nacimiento: str, provincia_nacimiento: str, email: str) -> None:
        self.id = _id
        self.usuario = usuario
        if "pbkdf2" in contrasenia:
            self.contrasenia = contrasenia
        else:
            self.set_password(contrasenia)
        self.fechaNacimiento = fecha_nacimiento
        self.nombre = nombre
        self.apellido = apellido
        self.ciudadNacimiento = ciudad_nacimiento
        self.provinciaNacimiento = provincia_nacimiento
        self.email = email

    def lst(self) -> Tuple:
        return (self.id, self.usuario, self.contrasenia, self.fechaNacimiento, self.nombre, self.apellido,
                self.ciudadNacimiento, self.provinciaNacimiento, self.email)

    def __repr__(self):
        return f"({self.id, self.usuario, self.contrasenia, self.fechaNacimiento, self.nombre, self.apellido, 
        self.ciudadNacimiento, self.provinciaNacimiento, self.email})"

    def set_password(self, password):
        self.contrasenia = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasenia, password)
from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    ciudad_nacimiento = models.CharField(max_length=100, blank=True)
    provincia_nacimiento = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    usuario = models.CharField(max_length=150, unique=True)
    contrasenia = models.CharField(max_length=150)
    sexo = models.CharField(max_length=10)

    class Meta:
        db_table = 'Usuario'  # nombre de la tabla en MySQL


class Asistente(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'Asistente'  # nombre de la tabla en MySQL


class DT(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'DT'  # nombre de la tabla en MySQL


class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    altura = models.FloatField()
    peso = models.FloatField()

    class Meta:
        db_table = 'Jugador'  # nombre de la tabla en MySQL


class Equipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=150)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=80)
    provincia = models.CharField(max_length=50)
    cant_victorias_local = models.IntegerField()
    cant_victorias_visit = models.IntegerField()
    campeonatos = models.IntegerField()
    campeones_actuales = models.BooleanField()

    class Meta:
        db_table = 'Equipo'


class EquipoAsistente(models.Model):
    id = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo')
    id_asistente = models.ForeignKey(Asistente, on_delete=models.CASCADE,db_column='id_asistente')
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    class Meta:
        db_table = 'Equipo_Asistente'


class EquipoDt(models.Model):
    id = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE,db_column='id_equipo')
    id_dt = models.ForeignKey(DT, on_delete=models.CASCADE, db_column='id_dt')
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    class Meta:
        db_table = 'Equipo_Dt'


class EquipoJugador(models.Model):
    id = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE,db_column='id_equipo')
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE,db_column='id_jugador')
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField()
    nro_jugador = models.IntegerField()
    posicion_pcpal = models.CharField(max_length=20)
    posicion_secundaria = models.CharField(max_length=20)

    class Meta:
        db_table = 'Equipo_Jugador'


class Formacion(models.Model):
    id = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo', related_name='formaciones')
    jugador_1 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_1', related_name='formaciones_jugador_1')
    jugador_2 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_2', related_name='formaciones_jugador_2')
    jugador_3 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_3', related_name='formaciones_jugador_3')
    jugador_4 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_4', related_name='formaciones_jugador_4')
    jugador_5 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_5', related_name='formaciones_jugador_5')
    jugador_6 = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='jugador_6', related_name='formaciones_jugador_6')
    libero = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='libero', related_name='formaciones_libero')

    class Meta:
        db_table = 'Formacion'


class Liga(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=20)
    ptos_x_victoria = models.IntegerField()
    ptos_x_32_vict = models.IntegerField()
    ptos_x_32_derrota = models.IntegerField()

    class Meta:
        db_table = 'Liga'


class Temporada(models.Model):
    id = models.AutoField(primary_key=True)
    anio_desde = models.IntegerField()
    anio_hasta = models.IntegerField()
    estado = models.CharField(max_length=20)
    id_liga = models.ForeignKey(Liga, on_delete=models.CASCADE,db_column='id_liga')

    class Meta:
        db_table = 'Temporada'


class Posiciones(models.Model):
    id = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE,db_column='id_equipo')
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE,db_column='id_temporada')
    puntaje = models.IntegerField()
    set_ganados = models.IntegerField()
    set_en_contra = models.IntegerField()
    diferencia_sets = models.IntegerField()

    class Meta:
        db_table = 'Posiciones'


class Partido(models.Model):
    id = models.AutoField(primary_key=True)
    id_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_local', related_name='partidos_local')
    fecha = models.DateField()
    hora = models.TimeField()
    set_ganados_local = models.IntegerField()
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada')
    set_ganados_visita = models.IntegerField()
    id_visita = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_visita', related_name='partidos_visita')

    class Meta:
        db_table = 'Partido'


class Estadisticas(models.Model):
    id = models.AutoField(primary_key=True)
    remates_fallidos = models.IntegerField()
    remates_buenos = models.IntegerField()
    defensas_fallidas = models.IntegerField()
    defensas_buenas = models.IntegerField()
    bloqueos_fallidos = models.IntegerField()
    bloqueos_buenos = models.IntegerField()
    saques_fallidos = models.IntegerField()
    saques_buenos = models.IntegerField()
    recepciones_buenas = models.IntegerField()
    recepciones_fallidas = models.IntegerField()
    fecha_carga = models.DateField()
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido', null=True, blank=True)
    id_asistente = models.ForeignKey(Asistente, on_delete=models.CASCADE, db_column='id_asistente')
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador')

    class Meta:
        db_table = 'Estadisticas'


class Set(models.Model):
    id = models.AutoField(primary_key=True)
    puntos_visita = models.IntegerField()
    puntos_local = models.IntegerField()
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido')
    nro_set = models.IntegerField()
    id_formacion_local = models.ForeignKey(Formacion, on_delete=models.CASCADE, db_column='id_formacion_local',
                                           related_name='id_formacion_local')
    id_formacion_visit = models.ForeignKey(Formacion, on_delete=models.CASCADE, db_column='id_formacion_visit',
                                           related_name='id_formacion_visit')

    class Meta:
        db_table = 'Set'


class Cambio(models.Model):
    id = models.AutoField(primary_key=True)
    id_jugador_sale = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador_sale',
                                        related_name='id_jugador_sale')
    id_jugador_entra = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador_entra',
                                         related_name='id_jugador_entra')
    id_formacion = models.ForeignKey(Formacion, on_delete=models.CASCADE, db_column='id_formacion')
    cerro = models.BooleanField()
    permanente = models.BooleanField()

    class Meta:
        db_table = 'Cambio'
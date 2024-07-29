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
    id_usuario = models.IntegerField()

    class Meta:
        db_table = 'Asistente'  # nombre de la tabla en MySQL


class DT(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.IntegerField()
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'DT'  # nombre de la tabla en MySQL


class Jugador(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.IntegerField()
    altura = models.FloatField()
    peso = models.FloatField()

    class Meta:
        db_table = 'Jugador'  # nombre de la tabla en MySQL

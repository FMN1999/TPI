from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    ciudad_nacimiento = models.CharField(max_length=100, blank=True)
    provincia_nacimiento = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

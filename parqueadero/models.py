from django.db import models

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_total = models.IntegerField(default=0)
    espacios_disponibles = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre
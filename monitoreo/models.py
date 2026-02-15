from django.db import models

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100)  # Ej: "Ingenierías"
    capacidad_total = models.IntegerField()    # Cuantos caben
    espacios_ocupados = models.IntegerField(default=0) # Cuantos hay

    # Esto calcula automáticamente cuántos libres quedan
    @property
    def espacios_libres(self):
        return self.capacidad_total - self.espacios_ocupados

    # Esto define si mostramos "Lleno" o "Disponible"
    @property
    def estado(self):
        if self.espacios_ocupados >= self.capacidad_total:
            return "Lleno"
        return "Disponible"

    def __str__(self):
        return f"{self.nombre} ({self.estado})"
from django.db import models

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_total = models.IntegerField(default=0)
    espacios_ocupados = models.IntegerField(default=0) 

    def __str__(self):
        return self.nombre

    # --- LÓGICA DINÁMICA ---
    @property
    def total_celdas_reales(self):
        return self.celda_set.count()

    @property
    def espacios_ocupados_reales(self):
        return self.celda_set.filter(esta_ocupada=True).count()

    @property
    def espacios_libres_reales(self):
        return self.total_celdas_reales - self.espacios_ocupados_reales

    @property
    def estado_actual(self):
        if self.espacios_libres_reales <= 0:
            return "Lleno"
        return "Disponible"

class Celda(models.Model):
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    esta_ocupada = models.BooleanField(default=False)
    placa = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.numero} - {self.parqueadero.nombre}"
    
    
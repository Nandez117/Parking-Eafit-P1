from django.db import models

class ParkingLot(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Parqueadero")
    total_spaces = models.IntegerField(verbose_name="Capacidad Total")
    available_spaces = models.IntegerField(verbose_name="Espacios Disponibles")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de Imagen (Opcional)")

    class Meta:
        verbose_name = "Parqueadero"
        verbose_name_plural = "Parqueaderos"

    def __str__(self):
        return f"{self.name} - {self.available_spaces}/{self.total_spaces} disponibles"

    @property
    def availability_percentage(self):
        if self.total_spaces > 0:
            return round((self.available_spaces / self.total_spaces) * 100, 1)
        return 0
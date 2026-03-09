from django.db import models

class TiempoEspera(models.Model):

    PARQUEADERO_CHOICES = [
        ('central',  'Parqueadero Central'),
        ('ing',      'Parqueadero Ingenieros'),
        ('idiomas',  'Parqueadero Idiomas'),
    ]

    parqueadero = models.CharField(
        max_length=20,
        choices=PARQUEADERO_CHOICES,
        unique=True,   # Solo un registro por parqueadero
        verbose_name='Parqueadero'
    )

    vehiculos_cola  = models.IntegerField(verbose_name='Vehículos en cola')
    flujo_vehiculos = models.FloatField(verbose_name='Flujo (veh/min)')

    tiempo_espera   = models.IntegerField(editable=False, verbose_name='Tiempo de espera (min)')

    def save(self, *args, **kwargs):
        if self.flujo_vehiculos > 0:
            self.tiempo_espera = round(self.vehiculos_cola / self.flujo_vehiculos)
        else:
            self.tiempo_espera = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_parqueadero_display()

    class Meta:
        verbose_name        = 'Tiempo de Espera'
        verbose_name_plural = 'Tiempos de Espera'
from django.contrib import admin
from .models import TiempoEspera

@admin.register(TiempoEspera)
class TiempoEsperaAdmin(admin.ModelAdmin):
    list_display  = ('parqueadero', 'vehiculos_cola', 'flujo_vehiculos', 'tiempo_espera')
    list_editable = ('vehiculos_cola', 'flujo_vehiculos')   # Edita directo desde la lista
    readonly_fields = ('tiempo_espera',)                    # Se calcula solo, no se toca
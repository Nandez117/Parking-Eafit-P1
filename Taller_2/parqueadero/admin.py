from django.contrib import admin
from .models import ParkingLot

# Registramos el modelo para poder verlo en el panel de administrador si lo necesitas luego
admin.site.register(ParkingLot)
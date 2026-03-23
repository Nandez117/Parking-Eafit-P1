from django.contrib import admin

from .models import Celda, Parqueadero

admin.site.register(Parqueadero)
admin.site.register(Celda)
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from monitoreo.views import dashboard_guardia,vista_central, vista_ingenieros, vista_idiomas, actualizar_estado_celda, generar_reporte_ia, enviar_reporte_correo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_guardia, name='dashboard'), 
    path('central/', vista_central, name='p_central'), 
    path('ingenieros/', vista_ingenieros, name='p_ingenieros'), 
    path('idiomas/', vista_idiomas, name='p_idiomas'),
    # --- RUTA PARA AJAX ---
    path('actualizar_celda/', actualizar_estado_celda, name='actualizar_celda'),
    # --- RUTAS REPORTE IA ---
    path('central/reporte/', generar_reporte_ia, name='reporte_ia'),
    path('central/reporte/enviar/', enviar_reporte_correo, name='enviar_reporte'),
]

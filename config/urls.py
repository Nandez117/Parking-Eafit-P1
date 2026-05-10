"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from monitoreo import views 

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Autenticación
    path('login/', views.login_dummy, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro_usuario, name='registro'),

    # --- PÁGINAS PRINCIPALES (VISTAS) ---
    path('', views.dashboard_guardia, name='dashboard'), 
    path('central/', views.vista_central, name='p_central'), 
    path('ingenieros/', views.vista_ingenieros, name='p_ingenieros'), 
    path('idiomas/', views.vista_idiomas, name='p_idiomas'),
    path('faq/', views.vista_faq, name='faq'),
    
    # --- OPERACIONES DE CELDAS (AJAX) ---
    path('actualizar_celda/', views.actualizar_estado_celda, name='actualizar_celda'),
    path('buscar_vehiculo/', views.buscar_mi_vehiculo, name='buscar_vehiculo'),
    
    # --- NÚCLEO DE INTELIGENCIA ARTIFICIAL (REPORTES) ---
    path('ia/reporte/individual/', views.ia_reporte_individual, name='ia_reporte_individual'),
    path('ia/reporte/comparativo/', views.ia_reporte_comparativo, name='ia_reporte_comparativo'),
    
    # --- FUNCIONES DINÁMICAS DE IA ---
    path('ia/estado/', views.ia_estado_frase, name='ia_estado'),
    path('ia/recomendar/', views.ia_recomendar, name='ia_recomendar'),
]
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Parqueadero, Celda # Aquí solo los traemos

def dashboard_guardia(request):
    parqueaderos_db = Parqueadero.objects.all()
    parqueaderos_procesados = []

    for p in parqueaderos_db:
        nombre_bonito = p.nombre.replace('parq_', '').replace('_', ' ').upper()

        parqueaderos_procesados.append({
            "nombre_mayuscula": nombre_bonito,
            "nombre_titulo": nombre_bonito.title(),
            "total": p.total_celdas_reales,
            "ocupados": p.espacios_ocupados_reales,
            "disponibles": p.espacios_libres_reales,
            "estado": p.estado_actual
        })

    return render(request, "dashboard.html", {"parqueaderos": parqueaderos_procesados})

@csrf_exempt
def actualizar_estado_celda(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        celda_id = data.get('id')
        nueva_placa = data.get('placa')
        
        celda = get_object_or_404(Celda, id=celda_id)
        
        # 1. Actualizar Celda
        if nueva_placa:
            celda.esta_ocupada = True
            celda.placa = nueva_placa.upper()
        else:
            celda.esta_ocupada = False
            celda.placa = None
        celda.save()

        # 2. Sincronizar Parqueadero
        p = celda.parqueadero
        p.espacios_ocupados = p.espacios_ocupados_reales
        p.save()
        
        return JsonResponse({'status': 'ok', 'mensaje': 'Celda y contadores actualizados'})
    
    return JsonResponse({'status': 'error'}, status=400)

def vista_central(request):
    p_central = Parqueadero.objects.filter(nombre__icontains='central').first()
    if p_central:
        todas_celdas = Celda.objects.filter(parqueadero=p_central).order_by('numero')
        context = {
            'celdas_a': todas_celdas.filter(numero__istartswith='A'),
            'celdas_b': todas_celdas.filter(numero__istartswith='B'),
            'celdas_c': todas_celdas.filter(numero__istartswith='C'),
            'celdas_d': todas_celdas.filter(numero__istartswith='D'),
            'celdas_e': todas_celdas.filter(numero__istartswith='E'),
            'celdas_f': todas_celdas.filter(numero__istartswith='F'),
            'celdas_g': todas_celdas.filter(numero__istartswith='G'),
            'celdas_h': todas_celdas.filter(numero__istartswith='H'),
        }
    else:
        context = {}
    return render(request, "p_central.html", context)

def vista_ingenieros(request):
    return render(request, "p_ingenieros.html")

def vista_idiomas(request):
    return render(request, "p_idiomas.html")
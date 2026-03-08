from django.shortcuts import render

# Create your views here.

def home(request):
    # Capacidades totales de cada parqueadero
    central_total = 200
    ingenieria_total = 120
    idiomas_total = 100

    # Espacios disponibles (reemplazar con datos reales de tu modelo/sensor)
    central_disponibles = 11
    ingenieria_disponibles = 100
    idiomas_disponibles = 100

    # Calcular porcentajes
    central_pct = round((central_disponibles / central_total) * 100, 1) if central_total else 0
    ingenieria_pct = round((ingenieria_disponibles / ingenieria_total) * 100, 1) if ingenieria_total else 0
    idiomas_pct = round((idiomas_disponibles / idiomas_total) * 100, 1) if idiomas_total else 0

    context = {
        'central_disponibles': central_disponibles,
        'central_total': central_total,
        'central_pct': central_pct,
        'ingenieria_disponibles': ingenieria_disponibles,
        'ingenieria_total': ingenieria_total,
        'ingenieria_pct': ingenieria_pct,
        'idiomas_disponibles': idiomas_disponibles,
        'idiomas_total': idiomas_total,
        'idiomas_pct': idiomas_pct,
    }
    return render(request, 'home.html', context)

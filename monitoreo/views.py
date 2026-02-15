from django.shortcuts import render
from .models import Parqueadero

def dashboard_guardia(request):
    parqueaderos = {
        "ingenieria": {
            "total": 120,
            "disponibles": 35,
        },
        "central": {
            "total": 200,
            "disponibles": 0,
        },
        "idiomas": {
            "total": 80,
            "disponibles": 12,
        },
    }

    # calcular ocupados
    for p in parqueaderos.values():
        p["ocupados"] = p["total"] - p["disponibles"]

    return render(request, "dashboard.html", {
        "parqueaderos": parqueaderos
    })

    

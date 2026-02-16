from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # Datos de los parqueaderos con espacios disponibles
    parkings = [
        {
            'nombre': 'Parqueadero Ingeniería',
            'disponibles': 45,
            'totales': 120,
            'imagen': 'comparedSpaces/ingenieria.jpg'
        },
        {
            'nombre': 'Parqueadero Central',
            'disponibles': 8,
            'totales': 200,
            'imagen': 'comparedSpaces/central.jpg'
        },
        {
            'nombre': 'Parqueadero Idiomas',
            'disponibles': 82,
            'totales': 100,
            'imagen': 'comparedSpaces/idiomas.jpg'
        },
    ]
    
    # Calcular porcentaje de disponibilidad y ordenar (más disponibles primero)
    for parking in parkings:
        parking['porcentaje'] = round((parking['disponibles'] / parking['totales']) * 100, 1)
    
    # Ordenar por espacios disponibles (de mayor a menor)
    parkings_ordenados = sorted(parkings, key=lambda x: x['disponibles'], reverse=True)
    
    context = {
        'parkings': parkings_ordenados
    }
    return render(request, 'home.html', context)
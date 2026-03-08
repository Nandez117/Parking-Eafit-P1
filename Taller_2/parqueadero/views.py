from django.shortcuts import render
from .models import ParkingLot

def home(request):
    # Trae todos los parqueaderos ordenados de mayor a menor disponibilidad (US-06)
    parking_lots = ParkingLot.objects.all().order_by('-available_spaces')

    context = {
        'parking_lots': parking_lots,
    }
    
    return render(request, 'home.html', context)
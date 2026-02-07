from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    context = {
        'central_TiempoDeEspera': 140,
        'ingenieria_TiempoDeEspera': 60,
        'idiomas_TiempoDeEspera': 6,
    }
    return render(request, 'home.html', context)
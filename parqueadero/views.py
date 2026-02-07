from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def home(request):
    context = {
        'central_disponibles': 76,
        'ingenieria_disponibles': 45,
        'idiomas_disponibles': 36,
    }
    return render(request, 'home.html', context)
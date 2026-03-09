from django.shortcuts import render
from .models import Parqueadero

def dashboard_guardia(request):
    # 1. Traemos los parqueaderos reales de la base de datos
    parqueaderos_db = Parqueadero.objects.all()

    # 2. Creamos una lista vacía para guardar los datos ya procesados y bonitos
    parqueaderos_procesados = []

    # 3. Recorremos lo que llegó de la base de datos
    for p in parqueaderos_db:
        
        # --- ARREGLAR EL NOMBRE ---
        # Si se llama "parq_central", le quitamos "parq_" y lo pasamos a MAYÚSCULAS -> "CENTRAL"
        nombre_bonito = p.nombre.replace('parq_', '').replace('_', ' ').upper()

        # --- ARMAR LOS DATOS PARA EL HTML ---
        # Aquí conservamos la estructura que te gusta, sacando los datos del modelo
        # y aprovechando las propiedades (cálculos) que ya le habías programado.
        datos_parqueadero = {
            "nombre_mayuscula": nombre_bonito,        # Ej: "CENTRAL"
            "nombre_titulo": nombre_bonito.title(),   # Ej: "Central" (para el subtítulo)
            "total": p.capacidad_total,
            "ocupados": p.espacios_ocupados,
            "disponibles": p.espacios_libres,         # Esto lo calcula tu modelo!
            "estado": p.estado                        # Esto también lo calcula tu modelo ("Lleno" o "Disponible")
        }
        
        # Añadimos este parqueadero ya procesado a nuestra lista
        parqueaderos_procesados.append(datos_parqueadero)

    # 4. Enviamos la lista procesada al HTML
    return render(request, "dashboard.html", {
        "parqueaderos": parqueaderos_procesados
    })
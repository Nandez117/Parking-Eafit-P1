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

from django.conf import settings
from django.core.mail import send_mail
import google.generativeai as genai
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

def generar_reporte_ia(request):
    p_central = Parqueadero.objects.filter(nombre__icontains='central').first()
    if not p_central:
        return render(request, "reporte_ia.html", {"error": "Parqueadero Central no encontrado."})
    
    todas_celdas = Celda.objects.filter(parqueadero=p_central)
    total_celdas = todas_celdas.count()
    ocupadas = todas_celdas.filter(esta_ocupada=True).count()
    libres = total_celdas - ocupadas
    
    zonas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    detalle_zonas = []
    for zona in zonas:
        celdas_zona = todas_celdas.filter(numero__istartswith=zona)
        ocupadas_z = celdas_zona.filter(esta_ocupada=True).count()
        totales_z = celdas_zona.count()
        detalle_zonas.append(f"Zona {zona}: {ocupadas_z}/{totales_z} ocupadas.")
    
    resumen_texto = "\n".join(detalle_zonas)
    
    prompt = f"""
    Actúa como un experto analista de infraestructuras y parqueaderos universitarios.
    A continuación se presentan los datos en tiempo real del Parqueadero Central:
    - Ocupación global: {ocupadas} de {total_celdas} celdas están ocupadas.
    - Celdas disponibles: {libres}.
    
    Desglose por zonas:
    {resumen_texto}
    
    Por favor, elabora un breve reporte profesional (max 300 palabras).
    Asegúrate de incluir recomendaciones sobre cómo distribuir mejor los vehículos.
    Formatea el texto en HTML puro (puedes usar <h3>, <p>, <ul>, <li>, <strong>) sin etiquetas Markdown de código cerradas, simplemente los tags HTML sueltos.
    """
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction="Eres el sistema de reportes del Parking EAFIT.")
        response = model.generate_content(prompt)
        reporte_html = response.text
        if reporte_html.startswith("```html"):
            reporte_html = reporte_html.replace("```html", "", 1).strip()
        if reporte_html.endswith("```"):
            reporte_html = reporte_html.rsplit("```", 1)[0].strip()

        request.session['ultimo_reporte'] = reporte_html
    except Exception as e:
        reporte_html = f"<p class='text-danger'>Error comunicándose con la IA: {str(e)}</p>"
        
    return render(request, "reporte_ia.html", {"reporte": mark_safe(reporte_html)})

def enviar_reporte_correo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        reporte_html = request.session.get('ultimo_reporte', 'No hay reporte generado.')
        
        try:
            send_mail(
                subject='Analítica e IA - Reporte de Parqueadero Central',
                message='',
                html_message=reporte_html,
                from_email='no-reply@parkingeafit.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f"¡Reporte enviado exitosamente a {email}!")
        except Exception as e:
            messages.error(request, f"Error enviando correo: {str(e)}")
            
    return redirect('reporte_ia')
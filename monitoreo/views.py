from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
import json
import re
import google.generativeai as genai
from .models import Parqueadero, Celda, Perfil
from .forms import RegistroForm

# ─────────────────────────────────────────
#  HELPERS PARA DATA E IA
# ─────────────────────────────────────────

def _get_parqueadero_data(parqueadero, horas=24):
    celdas = Celda.objects.filter(parqueadero=parqueadero)
    total   = celdas.count()
    ocupadas = celdas.filter(esta_ocupada=True).count()
    libres   = total - ocupadas

    zonas_letras = sorted(set(c.numero[0] for c in celdas if c.numero))
    detalle = []
    for z in zonas_letras:
        czs = celdas.filter(numero__istartswith=z)
        oc  = czs.filter(esta_ocupada=True).count()
        tt  = czs.count()
        porcentaje_zona = round(oc/tt*100 if tt else 0, 1)
        detalle.append(f"Zona {z}: {oc}/{tt} ocupadas ({porcentaje_zona}%)")

    return {
        "nombre": parqueadero.nombre,
        "total": total,
        "ocupadas": ocupadas,
        "libres": libres,
        "porcentaje": round((ocupadas / total * 100) if total else 0, 1),
        "detalle_zonas": detalle,
    }

def _periodo_label(horas: str) -> str:
    mapa = {
        "6":   "las últimas 6 horas",
        "12":  "las últimas 12 horas",
        "24":  "las últimas 24 horas",
        "168": "la última semana",
    }
    return mapa.get(str(horas), f"las últimas {horas} horas")

def _gemini_call(prompt: str) -> str:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    instruccion = (
        "Eres un analista experto en gestión de parqueaderos universitarios. "
        "Responde ÚNICAMENTE con código HTML válido usando clases Bootstrap 5. "
        "No incluyas explicaciones fuera del HTML, no uses markdown. "
        "Genera tablas con <table class='table table-bordered table-hover table-sm'>. "
        "NUNCA incluyas secciones de recomendaciones operativas.\n\n"
    )
    
    prompt_seguro = instruccion + prompt
    model = genai.GenerativeModel('gemini-2.5-flash') # Modelo actualizado y robusto
    response = model.generate_content(prompt_seguro)
    html = response.text.strip()
    
    if "```html" in html:
        html = html.split("```html")[1].split("```")[0].strip()
    elif "```" in html:
        html = html.split("```")[1].split("```")[0].strip()
        
    return html

def _prompt_individual(data: dict, horas: str) -> str:
    nombre   = data["nombre"].replace("parq_", "").replace("_", " ").title()
    detalle  = "\n".join(data["detalle_zonas"])
    periodo  = _periodo_label(horas)

    return f"""
Genera un reporte de ocupación para el Parqueadero {nombre} correspondiente a {periodo}.

Datos de ocupación actuales:
- Celdas totales: {data['total']}
- Celdas ocupadas: {data['ocupadas']} ({data['porcentaje']}%)
- Celdas libres: {data['libres']}

Detalle por zonas:
{detalle}

Estructura OBLIGATORIA del reporte (en HTML Bootstrap 5):
1. <h4> con el título del reporte indicando el parqueadero y el periodo.
2. Un párrafo introductorio describiendo el estado general de ocupación durante {periodo}.
3. Tabla de resumen global con columnas: Total | Ocupadas | Libres | % Ocupación.
4. Tabla de detalle por zonas con columnas: Zona | Ocupadas | Total | % Ocupación.
5. Un párrafo de conclusión sobre el comportamiento observado en {periodo}.
"""

def _prompt_comparativo(datos: list, horas: str) -> str:
    periodo = _periodo_label(horas)
    bloques = []
    for d in datos:
        nombre = d["nombre"].replace("parq_", "").replace("_", " ").title()
        zonas  = "\n  ".join(d["detalle_zonas"])
        bloques.append(
            f"• {nombre}: {d['ocupadas']}/{d['total']} ocupadas "
            f"({d['porcentaje']}%), {d['libres']} libres.\n  {zonas}"
        )
    texto = "\n".join(bloques)

    return f"""
Genera un reporte comparativo de ocupación de los 3 parqueaderos universitarios correspondiente a {periodo}.

Datos de ocupación actuales:
{texto}

Estructura OBLIGATORIA del reporte (en HTML Bootstrap 5):
1. <h4> con el título "Reporte Comparativo – {periodo.title()}".
2. Un párrafo introductorio con el análisis general del periodo {periodo}.
3. Tabla comparativa con columnas: Parqueadero | Total | Ocupadas | Libres | % Ocupación.
4. Un párrafo identificando el parqueadero con mayor ocupación y el de menor ocupación durante {periodo}, con análisis de la diferencia entre ellos.
5. Un párrafo de conclusión sobre la distribución global de vehículos en {periodo}.
"""

def _wrap_html(titulo: str, contenido_html: str) -> str:
    ahora = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>{titulo}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ font-family: 'Segoe UI', sans-serif; padding: 3rem; background: #fff; }}
    h4   {{ color: #0d1b3e; margin-bottom: 1rem; }}
    .footer-report {{ margin-top: 3rem; border-top: 1px solid #dee2e6; padding-top: 1rem; color: #6c757d; font-size: 0.85rem; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="d-flex align-items-center gap-3 mb-1">
      <h2 style="color:#0d1b3e; margin:0;">{titulo}</h2>
    </div>
    <p class="text-muted small mb-4">Generado el {ahora} &nbsp;|&nbsp; PARKING EAFIT</p>
    <hr class="mb-4">
    {contenido_html}
    <div class="footer-report text-center">
      PARKING EAFIT &middot; Universidad EAFIT &middot; Medellín, Colombia
    </div>
  </div>
  <script>window.onload = () => window.print();</script>
</body>
</html>"""

# ─────────────────────────────────────────
#  VISTAS PRINCIPALES Y MAPAS
# ─────────────────────────────────────────

@login_required
def dashboard_guardia(request):
    parqueaderos_db = Parqueadero.objects.all()
    parqueaderos_procesados = []
    for p in parqueaderos_db:
        nombre_bonito = p.nombre.replace('parq_', '').replace('_', ' ').upper()
        parqueaderos_procesados.append({
            "id": p.id,
            "nombre_mayuscula": nombre_bonito,
            "nombre_titulo": nombre_bonito.title(),
            "total": p.total_celdas_reales,
            "ocupados": p.espacios_ocupados_reales,
            "disponibles": p.espacios_libres_reales,
            "estado": p.estado_actual,
        })
    return render(request, "dashboard.html", {"parqueaderos": parqueaderos_procesados})

@csrf_exempt
@login_required
def actualizar_estado_celda(request):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permiso denegado'}, status=403)
        
    if request.method == 'POST':
        data  = json.loads(request.body)
        celda = get_object_or_404(Celda, id=data.get('id'))
        placa = data.get('placa')

        if placa:
            placa = placa.upper().strip()
            
            # Validación de formato de placa (3 letras, 3 números)
            if not re.match(r'^[A-Z]{3}\d{3}$', placa):
                return JsonResponse({'status': 'error', 'message': 'Formato de placa inválido. Debe ser 3 letras seguidas de 3 números (Ej: ABC123).'}, status=400)
            
            # Restricción por Pico y Placa
            dia_semana = timezone.now().weekday()
            ultimo_digito = int(placa[-1])
            pico_y_placa = {
                0: [1, 7], # Lunes
                1: [0, 3], # Martes
                2: [4, 6], # Miércoles
                3: [5, 9], # Jueves
                4: [2, 8], # Viernes
                5: [],     # Sábado
                6: []      # Domingo
            }
            if ultimo_digito in pico_y_placa.get(dia_semana, []):
                return JsonResponse({'status': 'error', 'message': 'El vehículo tiene Pico y Placa el día de hoy. Ingreso denegado.'}, status=400)

            celda.esta_ocupada, celda.placa = True, placa
        else:
            celda.esta_ocupada, celda.placa = False, None
        celda.save()

        p = celda.parqueadero
        p.espacios_ocupados = p.espacios_ocupados_reales
        p.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def vista_central(request):
    p = Parqueadero.objects.filter(nombre__icontains='central').first()
    context = {}
    if p:
        c = Celda.objects.filter(parqueadero=p).order_by('numero')
        for l in 'ABCDEFGHIJ':
            context[f'celdas_{l.lower()}'] = c.filter(numero__istartswith=l)
    return render(request, "p_central.html", context)

@login_required
def vista_ingenieros(request):
    p = Parqueadero.objects.filter(nombre__icontains='ingenieros').first()
    context = {}
    if p:
        c = Celda.objects.filter(parqueadero=p).order_by('numero')
        for l in 'ABCDEFGHIJK':
            context[f'celdas_{l.lower()}'] = c.filter(numero__istartswith=l)
    return render(request, "p_ingenieros.html", context)

@login_required
def vista_idiomas(request):
    p = Parqueadero.objects.filter(nombre__icontains='idiomas').first()
    context = {}
    if p:
        c = Celda.objects.filter(parqueadero=p).order_by('numero')
        for l in 'ABCDEFGHIJKLM':
            context[f'celdas_{l.lower()}'] = c.filter(numero__istartswith=l)
    return render(request, "p_idiomas.html", context)

def vista_faq(request):
    return render(request, "faq.html")

# ─────────────────────────────────────────
#  ENDPOINTS DE REPORTES IA
# ─────────────────────────────────────────

@csrf_exempt
@login_required
def ia_reporte_individual(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permiso denegado'}, status=403)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo peticiones POST'}, status=405)

    try:
        body     = json.loads(request.body)
        park_id  = body.get('parqueadero_id')
        horas    = str(body.get('horas', '24'))

        if horas not in ('6', '12', '24', '168'):
            return JsonResponse({'error': 'Periodo no válido. Usa 6, 12, 24 o 168.'}, status=400)

        parqueadero = Parqueadero.objects.get(id=int(park_id))

    except Parqueadero.DoesNotExist:
        return JsonResponse({'error': 'Parqueadero no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error en datos de entrada: {str(e)}'}, status=400)

    nombre_limpio = parqueadero.nombre.replace('parq_', '').replace('_', ' ').title()
    titulo        = f"Reporte de Ocupación – {nombre_limpio}"
    filename      = f"Reporte_{nombre_limpio.replace(' ', '_')}_{horas}h.html"

    # CACHÉ PARA EVITAR LÍMITE DE TOKENS
    cache_key = f"ia_report_ind_{park_id}_{horas}"
    html_completo = cache.get(cache_key)

    if not html_completo:
        data   = _get_parqueadero_data(parqueadero, int(horas))
        prompt = _prompt_individual(data, horas)

        try:
            reporte_html = _gemini_call(prompt)
        except Exception as e:
            return JsonResponse({'error': f'Error conectando con Gemini: {str(e)}'}, status=500)

        html_completo = _wrap_html(titulo, reporte_html)
        cache.set(cache_key, html_completo, timeout=600) # Caché por 10 minutos

    response = HttpResponse(html_completo, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@csrf_exempt
@login_required
def ia_reporte_comparativo(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permiso denegado'}, status=403)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo peticiones POST'}, status=405)

    try:
        body  = json.loads(request.body)
        horas = str(body.get('horas', '24'))

        if horas not in ('6', '12', '24', '168'):
            return JsonResponse({'error': 'Periodo no válido. Usa 6, 12, 24 o 168.'}, status=400)

    except Exception:
        horas = '24'

    cache_key = f"ia_report_comp_{horas}"
    html_completo = cache.get(cache_key)

    if not html_completo:
        parqueaderos = Parqueadero.objects.all()
        if not parqueaderos.exists():
            return JsonResponse({'error': 'No hay parqueaderos en la base de datos.'}, status=404)

        datos  = [_get_parqueadero_data(p, int(horas)) for p in parqueaderos]
        prompt = _prompt_comparativo(datos, horas)

        try:
            reporte_html = _gemini_call(prompt)
        except Exception as e:
            return JsonResponse({'error': f'Error conectando con Gemini: {str(e)}'}, status=500)

        titulo        = "Reporte Comparativo Global"
        html_completo = _wrap_html(titulo, reporte_html)
        cache.set(cache_key, html_completo, timeout=600) # Caché por 10 minutos

    response = HttpResponse(html_completo, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Comparativo_{horas}h.html"'
    return response

# ─────────────────────────────────────────
#  ENDPOINTS AUXILIARES (sin uso activo)
# ─────────────────────────────────────────

@csrf_exempt
def ia_estado_frase(request):
    return JsonResponse({'frase': ''})

@csrf_exempt
def ia_recomendar(request):
    return JsonResponse({'recomendacion': ''})

# ─────────────────────────────────────────
#  BÚSQUEDA DE VEHÍCULO
# ─────────────────────────────────────────

@login_required
def buscar_mi_vehiculo(request):
    try:
        placa = request.user.perfil.placa
        if not placa:
            return JsonResponse({'status': 'error', 'message': 'No tienes ninguna placa registrada en tu cuenta.'})
        
        celda = Celda.objects.filter(placa=placa.upper(), esta_ocupada=True).first()
        if celda:
            return JsonResponse({
                'status': 'ok',
                'parqueadero': celda.parqueadero.nombre.replace('parq_', '').title(),
                'celda': celda.numero,
                'placa': placa
            })
        else:
            return JsonResponse({'status': 'error', 'message': f'El vehículo con placa {placa} no se encuentra en el campus.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Debes registrar la placa en tu perfil para usar esta función.'})

# ─────────────────────────────────────────
#  SISTEMA DE AUTENTICACIÓN
# ─────────────────────────────────────────

def registro_usuario(request):
    # Si ya está logueado, lo mandamos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False # Nos aseguramos de que sea solo visitante
            user.save()
            
            # Crear el perfil con la placa
            placa = form.cleaned_data.get('placa', '').upper()
            Perfil.objects.create(user=user, placa=placa)
            
            login(request, user) # Iniciar sesión automáticamente tras registro
            return redirect('dashboard') # Redirigir al panel principal
    else:
        form = RegistroForm()
        
    return render(request, 'registro.html', {'form': form})

def login_dummy(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'estudiante')
        username_input = request.POST.get('username', '').strip()
        
        # Fallback si dejan el campo vacío
        if not username_input:
            username_input = 'admin_dummy' if tipo == 'admin' else 'invitado_dummy'
            
        if tipo == 'acceso_rapido':
            username_input = 'invitado_dummy'
            
        if tipo == 'admin':
            user, created = User.objects.get_or_create(username=username_input)
            if created or not user.is_staff:
                user.is_staff = True
                user.is_superuser = True
                user.save()
            login(request, user)
        else:
            user, created = User.objects.get_or_create(username=username_input)
            if created or user.is_staff:
                user.is_staff = False
                user.is_superuser = False
                user.save()
            login(request, user)
        return redirect('dashboard')
        
    return render(request, 'login.html')
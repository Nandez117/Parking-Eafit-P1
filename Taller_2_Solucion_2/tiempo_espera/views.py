from django.shortcuts import render
from .models import TiempoEspera

def build_context(request):
    def get_parking(key):
        try:
            return TiempoEspera.objects.get(parqueadero=key)
        except TiempoEspera.DoesNotExist:
            return None

    central = get_parking('central')
    ing     = get_parking('ing')
    idiomas = get_parking('idiomas')

    def nivel(obj):
        if obj is None:
            return 'green'
        w = obj.tiempo_espera
        if w <= 4:  return 'green'
        if w <= 10: return 'yellow'
        return 'red'

    def advice(obj):
        msgs = {
            'green':  'Puedes ingresar sin demora',
            'yellow': 'Considera esperar unos minutos',
            'red':    'Alta congestión — evalúa otra entrada',
        }
        return msgs[nivel(obj)]

    lvl_central = nivel(central)
    lvl_ing     = nivel(ing)
    lvl_idiomas = nivel(idiomas)

    waits = [
        central.tiempo_espera if central else 0,
        ing.tiempo_espera     if ing     else 0,
        idiomas.tiempo_espera if idiomas else 0,
    ]
    avg_wait = round(sum(waits) / 3)

    if avg_wait <= 4:    lvl_banner = 'green'
    elif avg_wait <= 10: lvl_banner = 'yellow'
    else:                lvl_banner = 'red'

    def flow_pct(obj):
        if obj is None: return 0
        return min(100, round((obj.vehiculos_cola / 20) * 100))

    return {
        'central':  central,
        'ing':      ing,
        'idiomas':  idiomas,
        'lvl_central':       lvl_central,
        'lvl_ing':           lvl_ing,
        'lvl_idiomas':       lvl_idiomas,
        'lvl_banner':        lvl_banner,
        'advice_central':    advice(central),
        'advice_ing':        advice(ing),
        'advice_idiomas':    advice(idiomas),
        'avg_wait':          avg_wait,
        'flow_pct_central':  flow_pct(central),
        'flow_pct_ing':      flow_pct(ing),
        'flow_pct_idiomas':  flow_pct(idiomas),
    }


def home(request):
    return render(request, 'home.html', build_context(request))


def tiempo_espera(request):
    return render(request, 'estimatedTime/tiempo_espera.html', build_context(request))
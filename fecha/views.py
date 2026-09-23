from django.shortcuts import render

DIAS_SEMANA = [
    'lunes',
    'martes',
    'miércoles',
    'jueves',
    'viernes',
    'sábado',
    'domingo',
]

MESES = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
]

DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0


def fecha_valida(anio, mes, dia):
    if mes < 1 or mes > 12:
        return False
    if anio == 1582 and mes == 10 and 5 <= dia <= 14:
        return False
    dias_mes = DIAS_POR_MES[mes - 1]
    if mes == 2 and es_bisiesto(anio):
        dias_mes = 29
    return 1 <= dia <= dias_mes


def parsear_fecha(texto):
    partes = texto.split('-')
    if len(partes) != 3:
        return None
    if not all(p.isdigit() for p in partes):
        return None
    anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    if not fecha_valida(anio, mes, dia):
        return None
    return anio, mes, dia


def dia_de_la_semana(anio, mes, dia):
    """Congruencia de Zeller. 0 = lunes ... 6 = domingo."""
    if mes < 3:
        mes += 12
        anio -= 1
    k = anio % 100
    j = anio // 100
    h = (dia + (13 * (mes + 1)) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    return (h + 5) % 7


def calcular_dia(request):
    contexto = {}

    if request.method == 'POST':
        fecha_str = request.POST.get('fecha', '').strip()

        if not fecha_str:
            contexto['error'] = 'Debes ingresar una fecha.'
        else:
            fecha = parsear_fecha(fecha_str)
            if fecha is None:
                contexto['error'] = 'La fecha ingresada no es válida.'
            else:
                anio, mes, dia = fecha
                indice = dia_de_la_semana(anio, mes, dia)
                contexto['fecha_formateada'] = f'{dia} de {MESES[mes - 1]} de {anio}'
                contexto['dia_semana'] = DIAS_SEMANA[indice]

    return render(request, 'fecha/index.html', contexto)

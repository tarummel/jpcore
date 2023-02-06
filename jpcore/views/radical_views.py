from http import HTTPStatus
from django.db import connection
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, Radical
from jpcore.serializers import KanjiSerializer, RadicalSerializer


PAGE_LIMIT = 1000
NO_KANJI_FIELDS = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes']

def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

# returns all Radicals
# option 'simple' maps the response to { strokes -> [rad1, rad2, ...] }
@require_GET
def list(request):
    queryset = Radical.objects.all().order_by('strokes')
    
    if request.GET.get('simple', False):
        output = {}
        for row in queryset.iterator():
            strokes, radical = row.strokes, row.radical
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(radical)
        return success(HTTPStatus.OK, output)

    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

# returns the Radical object associated with the radical char
@require_GET
def get(request, radical):

    if len(radical) != 1:
        return error(HTTPStatus.BAD_REQUEST)
    
    try:
        queryset = Radical.objects.get(radical = radical)
    except:
        return error(HTTPStatus.NOT_FOUND, 'radical not found')
    
    serializer = RadicalSerializer(queryset, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

# returns all Kanji matching the complete list of comma-delimited Radicals
# option 'simple' maps the response to { strokes -> [rad1, rad2, ...] }
@require_GET
def getKanjiFromRadicals(request, radicals):

    if len(radicals) > 27:
        return error(HTTPStatus.BAD_REQUEST, 'either no radicals found or too many provided')

    split = [*set(radicals.split(','))]

    for s in split:
        if len(s) != 1:
            return error(HTTPStatus.BAD_REQUEST, 'one radical between commas only')
    
    queryset = Kanji.objects.annotate(
        c = Count('radicals', filter=Q(radicals__radical__in=split))).filter(c=len(split)
    ).order_by('strokes')[0:PAGE_LIMIT]

    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no kanji found')
    
    if request.GET.get('simple', False):
        output = {}
        for row in queryset.iterator():
            strokes, kanji = row.strokes, row.kanji
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(kanji)
        return success(HTTPStatus.OK, output)
    
    serializer = KanjiSerializer(queryset, many = True, fields = ['kanji', 'strokes'])
    return success(HTTPStatus.OK, serializer.data)

# returns a list of all viable Radicals from a given comma-delimited list of Radicals
@require_GET
def getRelatedRadicals(request, radicals):

    if len(radicals) > 27:
        return error(HTTPStatus.BAD_REQUEST, 'either no radicals found or too many provided')

    split = [*set(radicals.split(','))]

    for s in split:
        if len(s) != 1:
            return error(HTTPStatus.BAD_REQUEST, 'one radical between commas only')

    queryset = Radical.objects.filter(
        kanji__in = Kanji.objects.annotate(c = Count('radicals', filter=Q(radicals__radical__in=split))).filter(c=len(split))
    ).exclude(radical__in = split).distinct()
    
    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no kanji found')

    if request.GET.get('simple', False):
        output = ''
        for row in queryset.iterator():
            output += row.radical
        return success(HTTPStatus.OK, output)

    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

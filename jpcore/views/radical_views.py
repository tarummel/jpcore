from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, Radical
from jpcore.serializers import KanjiSerializer, RadicalSerializer

NO_KANJI_FIELDS = ['number', 'radical', 'strokes', 'meaning', 'reading', 'frequency', 'position', 'notes']

def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)


@require_GET
def list(request):
    queryset = Radical.objects.all()
    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

@require_GET
def get(request, radical):
    if len(radical) == 1:
        try:
            queryset = Radical.objects.get(radical = radical)
        except:
            return error(HTTPStatus.NOT_FOUND, 'radical not found')
        
        serializer = RadicalSerializer(queryset, fields = NO_KANJI_FIELDS)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

# TODO: Kanji returned should have keb, reb, glosses?
@require_GET
def getKanjiByRadical(request, radicals):
    valid = True
    split = radicals.split(',')

    for s in split:
        if len(s) != 1:
            valid = False
            
    if valid:
        queryset = Kanji.objects.filter(radicals__radical__in = split).distinct()
        if not len(queryset):
            return error(HTTPStatus.NOT_FOUND, 'no kanji found')
        
        serializer = KanjiSerializer(queryset, many = True, fields = ['kanji', 'strokes'])
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

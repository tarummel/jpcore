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

# returns all Radicals
@require_GET
def list(request):
    option = request.GET.get('option', '')

    if option == 'by_stroke_count':
        output = {}
        queryset = Radical.objects.all().values('strokes', 'radical')
        
        for row in queryset.iterator():
            strokes, radical = row['strokes'], row['radical']
            if not strokes in output:
                output[strokes] = ''
            output[strokes] += radical
        return success(HTTPStatus.OK, output)

    queryset = Radical.objects.all()
    serializer = RadicalSerializer(queryset, many = True, fields = NO_KANJI_FIELDS)
    return success(HTTPStatus.OK, serializer.data)

# returns the Radical object associated with the radical char
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

# returns all Kanji associated with a list of comma-delimited radical chars
@require_GET
def getKanjiByRadical(request, radicals):
    valid = True
    split = radicals.split(',')
    option = request.GET.get('option', '')

    for s in split:
        if len(s) != 1:
            valid = False
            
    if valid:
        queryset = Kanji.objects.filter(radicals__radical__in = split).distinct()

        if not len(queryset):
            return error(HTTPStatus.NOT_FOUND, 'no kanji found')
        
        if option == 'by_stroke_count':
            output = {}
            for row in queryset.iterator():
                strokes, kanji = row.strokes, row.kanji
                if not strokes in output:
                    output[strokes] = ''
                output[strokes] += kanji
            return success(HTTPStatus.OK, output)
        
        serializer = KanjiSerializer(queryset, many = True, fields = ['kanji', 'strokes'])
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

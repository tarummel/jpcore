from http import HTTPStatus
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, KDKanji
from jpcore.serializers import KDKanjiSerializer


PAGE_LIMIT = 500
MAX_RADICALS_LIMIT = 27

def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

# returns the KanjiDic kanji by id
@require_GET
def getById(request, id):
    try:
        kanji = KDKanji.objects.get(id = id)
    except Exception as e:
        return error(HTTPStatus.NOT_FOUND, 'entry by id not found')
    
    serializer = KDKanjiSerializer(kanji)
    return success(HTTPStatus.OK, serializer.data)

# returns the KanjiDic kanji by kanji
@require_GET
def getByKanji(request, kanji):
    if len(kanji) == 1:
        try:
            kanji = KDKanji.objects.get(kanji = kanji)
        except Exception as e:
            return error(HTTPStatus.NOT_FOUND, 'entry by kanji not found')
        
        serializer = KDKanjiSerializer(kanji)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

# returns all KDKanji matching the complete list of comma-delimited Radicals
# option 'simple' maps the response to { strokes -> [rad1, rad2, ...] }
@require_GET
def getKanjiFromRadicals(request, radicals):

    if len(radicals) > MAX_RADICALS_LIMIT:
        return error(HTTPStatus.BAD_REQUEST, 'either no radicals found or too many provided')

    split = [*set(radicals.split(','))]

    for s in split:
        if len(s) != 1:
            return error(HTTPStatus.BAD_REQUEST, 'one radical between commas only')

    queryset = KDKanji.objects.filter(kanji__in = Kanji.objects.annotate(
        c = Count('radicals', filter=Q(radicals__radical__in=split))).filter(c = len(split)
    ).values('kanji'))[:PAGE_LIMIT]

    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no matching entries found')

    if request.GET.get('simple', None):
        output = {}
        for row in queryset.values_list('kanji', 'kdmisc__strokes').iterator():
            kanji, strokes = row[0], row[1]
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(kanji)
        return success(HTTPStatus.OK, output)

    serializer = KDKanjiSerializer(queryset, many = True)
    return success(HTTPStatus.OK, serializer.data)

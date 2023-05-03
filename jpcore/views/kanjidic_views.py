from http import HTTPStatus
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, KDKanji, SkipCode, VisualCloseness
from jpcore.serializers import KDKanjiSerializer, VisualClosenessSerializer


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

    if request.GET.get('simple'):
        output = {}
        for row in queryset.values_list('kanji', 'kdmisc__strokes').iterator():
            kanji, strokes = row[0], row[1]
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(kanji)
        return success(HTTPStatus.OK, output)

    serializer = KDKanjiSerializer(queryset, many = True)
    return success(HTTPStatus.OK, serializer.data)

@require_GET
def getKanjiRandom(request):
    if request.GET.get('kanji_only', None):
        kanji = KDKanji.objects.order_by('?').values_list('kanji', flat = True).first()
        return success(HTTPStatus.OK, kanji)

    kanji = KDKanji.objects.order_by('?').first()
    serializer = KDKanjiSerializer(kanji)
    return success(HTTPStatus.OK, serializer.data)

@require_GET
def getKanjiBySkipCode(request, skip):
    
    try:
        values = [int(val) for val in skip.split('-')]
    except Exception as e:
        return error(HTTPStatus.BAD_REQUEST, 'malformed skip code')

    if not len(values) == 3:
        return error(HTTPStatus.BAD_REQUEST, 'malformed skip code')

    if not values[0] in [1, 2, 3, 4]:
        return error(HTTPStatus.BAD_REQUEST, 'invalid skip category (first number), must be 1 through 4')

    if values[1] < 1 or values[2] < 1:
        return error(HTTPStatus.BAD_REQUEST, 'main/sub (second/third numbers) values must be positive, non-zero number')

    try:
        mainRange = int(request.GET.get('main_range', 0))
        subRange = int(request.GET.get('sub_range', 0))
    except Exception as e:
        return error(HTTPStatus.BAD_REQUEST, 'range values must be whole, non-negative number')
    
    if mainRange < 0 or subRange < 0:
        return error(HTTPStatus.BAD_REQUEST, 'range values cannot be negative')

    mrange = (values[1] - mainRange, values[1] + mainRange) 
    srange = (values[2] - subRange, values[2] + subRange)
    queryset = KDKanji.objects.filter(skipcode__in = SkipCode.objects.filter(category = values[0], main__range = mrange, sub__range = srange)).distinct()[:PAGE_LIMIT]

    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no matching entries found')
    
    if request.GET.get('simple'):
        output = {}
        for query in queryset:
            kanji, strokes = query.kanji, query.kdmisc.first().strokes
            if not strokes in output:
                output[strokes] = []
            output[strokes].append(kanji)
        return success(HTTPStatus.OK, output)
    
    serializer = KDKanjiSerializer(queryset, many = True)
    return success(HTTPStatus.OK, serializer.data)  

@require_GET
def getVisualClosenessByKanji(request, kanji):

    if not len(kanji) == 1:
        return error(HTTPStatus.BAD_REQUEST, 'expected one (1) kanji character')

    try:
        sensitivity = float(request.GET.get('sensitivity', 0))
    except Exception as e:
        return error(HTTPStatus.BAD_REQUEST, 'sensitivity must be a float value between 0.000 through 1.000')
    
    if sensitivity < 0 or sensitivity > 1:
        return error(HTTPStatus.BAD_REQUEST, 'sensitivity must be between 0.000 through 1.000')

    try:
        queryset = VisualCloseness.objects.filter(sed__gte = sensitivity, left = KDKanji.objects.get(kanji = kanji))
    except Exception as e:
        return error(HTTPStatus.NOT_FOUND, 'kanji not found')

    if not len(queryset):
        return error(HTTPStatus.NOT_FOUND, 'no visual closeness record found')

    if request.GET.get('simple'):
        output = {}
        for query in queryset:
            kanji, sed = query.right.kanji, query.sed
            output[kanji] = sed
        return success(HTTPStatus.OK, output)

    serializer = VisualClosenessSerializer(queryset, many = True)
    return success(HTTPStatus.OK, serializer.data)
    
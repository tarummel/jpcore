from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import KDKanji
from jpcore.serializers import KDKanjiSerializer


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

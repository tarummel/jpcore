from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Kanji, Radical
from jpcore.serializers import KanjiSerializer


def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

@require_GET
def get(request, kanji):
    if len(kanji) == 1:
        try:
            queryset = Kanji.objects.get(kanji = kanji)
        except:
            return error(HTTPStatus.NOT_FOUND, 'kanji not found')
        
        serializer = KanjiSerializer(queryset)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)
    
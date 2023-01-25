from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import JMdictKanji
from jpcore.serializers import JMdictEntrySerializer


def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

# returns the complete JMdict entry for a given kanji char
@require_GET
def get(request, kanji):
    if len(kanji) == 1 and not kanji == '':
        try:
            entry = JMdictKanji.objects.select_related('entry').get(content = kanji).entry
        except:
            return error(HTTPStatus.NOT_FOUND, 'kanji not found')
        
        serializer = JMdictEntrySerializer(entry)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

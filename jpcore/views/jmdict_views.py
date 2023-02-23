from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import JMdictEntry, JMdictKanji
from jpcore.serializers import JMdictEntrySerializer


def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)

# returns the JMdict entry by id
@require_GET
def getById(request, id):
    try:
        entry = JMdictEntry.objects.get(ent_seq = id)
    except Exception as e:
        # print(e)
        return error(HTTPStatus.NOT_FOUND, 'entry not found')
    
    serializer = JMdictEntrySerializer(entry)
    return success(HTTPStatus.OK, serializer.data)

# returns all JMdict entries for a given kanji char
@require_GET
def getByKanji(request, kanji):
    if len(kanji) == 1 and not kanji == '':
        queryset = JMdictEntry.objects.filter(jkanji__content = kanji)

        if not len(queryset):
            return error(HTTPStatus.NOT_FOUND, 'entry not found')
        
        serializer = JMdictEntrySerializer(queryset, many = True)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

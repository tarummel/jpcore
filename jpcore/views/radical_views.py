from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from jpcore.models import Radical
from jpcore.serializers import RadicalSerializer


def success(code, data):
    return JsonResponse({'status': 'success', 'data': data}, status = code)

def error(code, reason = None):
    if reason:
        return JsonResponse({'status': 'failed', 'reason': reason}, status = code)
    return JsonResponse({'status': 'failed'}, status = code)


@require_GET
def list(request):
    queryset = Radical.objects.all()
    serializer = RadicalSerializer(queryset, many = True)
    return success(HTTPStatus.OK, serializer.data)

@require_GET
def get(request, radical):
    if len(radical) == 1:
        try:
            queryset = Radical.objects.get(radical = radical)
        except:
            return error(HTTPStatus.NOT_FOUND, 'radical not found')
        
        serializer = RadicalSerializer(queryset)
        return success(HTTPStatus.OK, serializer.data)

    return error(HTTPStatus.BAD_REQUEST)

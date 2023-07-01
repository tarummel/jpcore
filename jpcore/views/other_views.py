from http import HTTPStatus
from django.http import HttpResponse
from django.views.decorators.http import require_GET


# TODO: add DB + other checks 
@require_GET
def getHealthcheck(request):
    return HttpResponse('healthchecked', status=HTTPStatus.OK)

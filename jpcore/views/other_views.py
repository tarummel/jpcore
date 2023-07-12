from http import HTTPStatus
from logging import getLogger
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache

PING_NAME = 'ping'
PING_VALUE = 'test'
PING_TTL = 1800

log = getLogger(__name__)

def pingCache():
    cache.set(PING_NAME, PING_VALUE, PING_TTL)
    if not cache.get(PING_NAME):
        log.warn(f'Memcached ping failed')
        return False
    return True

def pingDB():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as error:
        log.warn(f'PSQL ping failed: {error}')
        return False

@require_GET
def getHealthcheck(request):
    db = pingDB()
    memcached = pingCache()
    status = HTTPStatus.OK if db and memcached else HTTPStatus.INTERNAL_SERVER_ERROR
    return JsonResponse({'db': db, 'memcached': memcached}, status = status)

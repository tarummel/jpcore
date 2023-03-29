from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from jpcore import views


CACHE_TIMEOUT=300

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include([
        path('jmdict/', include([
            path('kanji/<int:id>/', cache_page(CACHE_TIMEOUT)(views.jmdict_views.getById)),
            path('kanji/<str:kanji>/', cache_page(CACHE_TIMEOUT)(views.jmdict_views.getByKanji)),
        ])),    
        path('kanjidic/', include([
            path('kanji/<int:id>/', cache_page(CACHE_TIMEOUT)(views.kanjidic_views.getById)),
            path('kanji/skipcode/<str:skip>/', cache_page(CACHE_TIMEOUT)(views.kanjidic_views.getKanjiBySkipCode)),
            path('kanji/<str:kanji>/', cache_page(CACHE_TIMEOUT)(views.kanjidic_views.getByKanji)),
            path('radicals/<str:radicals>/kanji/', cache_page(CACHE_TIMEOUT)(views.kanjidic_views.getKanjiFromRadicals)),
            path('random/', views.kanjidic_views.getKanjiRandom),
        ])),
        path('krad/', include([
            path('radicals/', cache_page(CACHE_TIMEOUT)(views.krad_views.list)),
            path('radicals/<str:radical>/', cache_page(CACHE_TIMEOUT)(views.krad_views.getByRadical)),
            path('radicals/<str:radicals>/related/', cache_page(CACHE_TIMEOUT)(views.krad_views.getRelatedRadicals)),
        ])),
    ])),
]

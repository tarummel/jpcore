from django.contrib import admin
from django.urls import path, include

from jpcore import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include([
        path('jmdict/', include([
            path('kanji/<int:id>/', views.jmdict_views.getById),
            path('kanji/<str:kanji>/', views.jmdict_views.getByKanji),
        ])),    
        path('kanjidic/', include([
            path('kanji/<int:id>/', views.kanjidic_views.getById),
            path('kanji/<str:kanji>/', views.kanjidic_views.getByKanji),
            path('radicals/<str:radicals>/kanji/', views.kanjidic_views.getKanjiFromRadicals),
            path('random/', views.kanjidic_views.getKanjiRandom),
        ])),
        path('krad/', include([
            path('radicals/', views.krad_views.list),
            path('radicals/<str:radical>/', views.krad_views.getByRadical),
            path('radicals/<str:radicals>/related/', views.krad_views.getRelatedRadicals),
        ])),
    ])),
]

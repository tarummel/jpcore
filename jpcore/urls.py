from django.contrib import admin
from django.urls import path, include

from jpcore import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include([
        path('radicals/', views.radical_views.list),
        path('radicals/<str:radical>/', views.radical_views.get),
        path('radicals/<str:radicals>/kanji/', views.radical_views.getKanjiFromRadicals),
        path('radicals/<str:radicals>/related/', views.radical_views.getRelatedRadicals),
        path('kanji/<str:kanji>/', views.kanji_views.get),
    ])),
]

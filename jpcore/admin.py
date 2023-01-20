from django.contrib import admin

from jpcore import models

admin.site.register(models.JMdictEntry)
admin.site.register(models.JMdictKanji)
admin.site.register(models.JMdictReading)
admin.site.register(models.JMdictSense)
admin.site.register(models.JMdictGlossary)
admin.site.register(models.JMdictSource)

admin.site.register(models.Radical)
admin.site.register(models.Kanji)

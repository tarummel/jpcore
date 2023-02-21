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

admin.site.register(models.KDKanji)
admin.site.register(models.KDCodePoint)
admin.site.register(models.KDRadical)
admin.site.register(models.KDMisc)
admin.site.register(models.KDVariant)
admin.site.register(models.KDIndex)
admin.site.register(models.KDReading)
admin.site.register(models.KDMeaning)

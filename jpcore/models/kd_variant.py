from django.db import models


# Either a cross-reference code to another kanji, usually regarded as a variant, or an alternative indexing code for the
# current kanji.
class KDVariant(models.Model):
    
    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kvariant')

    deroo = models.TextField(blank = True)
    jis208 = models.TextField(blank = True)
    jis212 = models.TextField(blank = True)
    jis213 = models.TextField(blank = True)
    nelson = models.TextField(blank = True)
    njecd = models.TextField(blank = True)
    oneill = models.TextField(blank = True)
    sh = models.TextField(blank = True)

    def __str__(self):
        return f'jis208: {self.jis208}'

from django.contrib.postgres.fields import ArrayField
from django.db import models


# The meaning associated with the kanji.
class KDMeaning(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdmeaning')

    # the English meaning (implied)
    en = ArrayField(models.TextField(), blank = True)
    
    def __str__(self):
        return f'eng: {self.en}'

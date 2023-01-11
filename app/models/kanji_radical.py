from django.db import models

# Kanji with an associated Radical, one at a time
class KanjiRadical(models.Model):
    kanji = models.CharField(max_length = 1)
    radical = models.CharField(max_length = 1)

    def __str__(self):
        return f' \
            kan: {self.kanji} \
            rad: {self.radical} \
        '
from django.db import models

class Radical(models.Model):
    number = models.IntegerField()
    part = models.CharField(max_length = 1)
    strokes = models.IntegerField()

    def __str__(self):
        return f' \
            kan: {self.kanji} \
            rad: {self.radical} \
        '
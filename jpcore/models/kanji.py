from django.db import models


# Kanji fields derived from a combination of the kradfile, radinfo, kinfo (TODO)
class Kanji(models.Model):
    kanji = models.TextField()
    radicals = models.ManyToManyField('Radical')
    strokes = models.IntegerField() # sum of radical strokes

    def __str__(self):
        return f'kanji: {self.kanji}, rads: {self.radicals}, strokes: {self.strokes}'

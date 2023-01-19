from django.db import models

class Kanji(models.Model):
    kanji = models.TextField()
    radicals = models.ManyToManyField('Radical')
    strokes = models.IntegerField() # sum of radicals

    def __str__(self):
        return f'kanji: {self.kanji}, rads: {self.radicals}, strokes: {self.strokes}'

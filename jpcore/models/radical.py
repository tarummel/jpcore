from django.db import models


# Radical derived from a combination of the kradfile and radinfo
class Radical(models.Model):
    number = models.IntegerField(blank = True, null = True) # Kangxi dict number
    radical = models.TextField()
    strokes = models.IntegerField()
    meaning = models.TextField()
    reading = models.TextField()
    position = models.TextField(blank = True)
    frequency = models.IntegerField()
    notes = models.TextField(blank = True)
    # kanji_set = reverse mapping to Kanji's M2M relationship

    def __str__(self):
        return f'No: {self.number}, rad: {self.radical}, stks: {self.strokes}, mean: {self.meaning}, read: {self.reading}, pos: {self.position}, note: {self.notes}'

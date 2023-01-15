from django.db import models

class Radical(models.Model):
    number = models.IntegerField(blank = True) # Kangxi dict number
    radical = models.TextField()
    strokes = models.IntegerField()
    meaning = models.TextField()
    reading = models.TextField()
    position = models.TextField(blank = True)
    frequency = models.IntegerField()
    notes = models.TextField(blank = True)

    def __str__(self):
        return f' \
            kan: {self.number} \
            rad: {self.radical} \
            st#: {self.strokes} \
            mea: {self.meaning} \
            rea: {self.reading} \
            pos: {self.position} \
            note: {self.notes} \
        '
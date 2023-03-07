from django.db import models


# Aux table for KDKanji meant for faster computation
# composite key cannot be the primary per django docs so implicit id is pkey instead
class SkipCode(models.Model):

    kanji = models.ManyToManyField('KDKanji')

    category = models.IntegerField()
    main = models.IntegerField()
    sub = models.IntegerField()

    class Meta:
        unique_together = ['category', 'main', 'sub']

    def __str__(self):
        return f'skip: {self.category}-{self.main}-{self.sub}'

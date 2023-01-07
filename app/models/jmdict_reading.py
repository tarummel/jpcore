from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictReading(models.Model):
    entry = models.ForeignKey('JMdictEntry', on_delete = models.CASCADE)

    element = models.TextField(blank = False)
    no_kanji = models.BooleanField(blank = False, null = False)
    restrictions = models.TextField(blank = True)
    information = models.TextField(blank = True)
    priorities = ArrayField(models.CharField(blank = True, max_length = 8), size = 8)

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.entry.ent_seq,
            self.element,
            self.no_kanji,
            self.restrictions,
            self.information,
            self.priorities,
        )
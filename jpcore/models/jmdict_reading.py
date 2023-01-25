from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictReading(models.Model):
    entry = models.ForeignKey('JMdictEntry', related_name = 'jreading', on_delete = models.CASCADE)

    content = models.TextField()
    no_kanji = models.BooleanField(blank = True)
    restrictions = models.TextField(blank = True)
    information = models.TextField(blank = True)
    priorities = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, con: {self.content}, nok: {self.no_kanji}, restr: {self.restrictions}, inf: {self.information}, pri: {self.priorities}'

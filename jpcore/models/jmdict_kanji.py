from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictKanji(models.Model):
    entry = models.ForeignKey('JMdictEntry', related_name = 'jkanji', on_delete = models.CASCADE)

    content = models.TextField(blank = True)
    information = models.TextField(blank = True)
    priorities = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, con: {self.content}, inf: {self.information}, pri: {self.priorities}'

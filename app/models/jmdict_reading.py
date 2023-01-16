from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictReading(models.Model):
    entry = models.ForeignKey('JMdictEntry', on_delete = models.CASCADE)

    content = models.TextField()
    no_kanji = models.BooleanField(blank = True)
    restrictions = models.TextField(blank = True)
    information = models.TextField(blank = True)
    priorities = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f' \
            entry: {self.entry.ent_seq}, \
            elem: {self.content}, \
            noka: {self.no_kanji}, \
            rest: {self.restrictions}, \
            info: {self.information}, \
            prio: {self.priorities} \
        '

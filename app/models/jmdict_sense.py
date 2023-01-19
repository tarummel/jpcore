from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictSense(models.Model):
    entry = models.ForeignKey('JMdictEntry', on_delete = models.CASCADE)

    xreferences = ArrayField(models.TextField(), blank = True)
    antonyms = ArrayField(models.TextField(), blank = True)
    parts_of_speech = ArrayField(models.TextField(), blank = True)
    fields = ArrayField(models.TextField(), blank = True)
    misc = ArrayField(models.TextField(), blank = True)
    dialects = ArrayField(models.TextField(), blank = True)
    information = models.TextField(blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, xref: {self.xreferences}, ant: {self.antonyms}, fie: {self.fields}, misc: {self.misc}, dia: {self.dialects}, inf: {self.information}'

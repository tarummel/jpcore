from django.db import models

class JMdictEntry(models.Model):
    ent_seq = models.IntegerField(primary_key = True, editable = False, null = False)

    def __str__(self):
        return f'ent_seq: {self.ent_seq}'

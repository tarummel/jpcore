from django.db import models

class JMdictEntry(models.Model):
    ent_seq = models.IntegerField(primary_key = True, editable = False, blank = False, null = False)

    def __str__(self):
        return "{}".format(
            self.ent_seq,
        )
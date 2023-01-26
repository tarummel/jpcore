from django.db import models


# Entries consist of kanji elements, reading elements, general information and sense elements. 
# Each entry must have at least one reading element and one sense element. Others are optional.
class JMdictEntry(models.Model):
    # Unique numeric sequence number
    ent_seq = models.IntegerField(primary_key = True, editable = False, null = False)

    def __str__(self):
        return f'ent_seq: {self.ent_seq}'

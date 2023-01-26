from django.contrib.postgres.fields import ArrayField
from django.db import models


# The sense element will record the translational equivalent of the Japanese word, plus other related information. 
# Where there are several distinctly different meanings of the word, multiple sense elements will be employed.
class JMdictSense(models.Model):
    entry = models.ForeignKey('JMdictEntry', related_name = 'jsense', on_delete = models.CASCADE)

    # Used to indicate a cross-reference to another entry with a similar or related meaning or sense.
    xreferences = ArrayField(models.TextField(), blank = True)
    # Used to indicate another entry which is an antonym of the current entry/sense.
    antonyms = ArrayField(models.TextField(), blank = True)
    # Part-of-speech information about the entry/sense.
    parts_of_speech = ArrayField(models.TextField(), blank = True)
    # Information about the field of application of the entry/sense if applicable.
    fields = ArrayField(models.TextField(), blank = True)
    # Used for other relevant information about the entry/sense.
    misc = ArrayField(models.TextField(), blank = True)
    # For words specifically associated with regional dialects in Japanese.
    dialects = ArrayField(models.TextField(), blank = True)
    # Additional information to be recorded about a sense.
    information = models.TextField(blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, xref: {self.xreferences}, ant: {self.antonyms}, fie: {self.fields}, misc: {self.misc}, dia: {self.dialects}, inf: {self.information}'

from django.contrib.postgres.fields import ArrayField
from django.db import models


# The reading element typically contains the valid readings of the word(s) in the kanji element using modern kanadzukai.
# Where there are multiple reading elements, they will typically be alternative readings of the kanji element. 
# In the absence of a kanji element, i.e. in the case of a word or phrase written entirely in kana, these elements will define the entry.
class JMdictReading(models.Model):
    entry = models.ForeignKey('JMdictEntry', related_name = 'jreading', on_delete = models.CASCADE)

    # Kanji reading with content restricted to kana and related characters such as chouon and kurikaeshi.
    content = models.TextField()
    # Content cannot be regarded as a true reading of the kanji typically used for words such as foreign place names and gairaigo.
    no_kanji = models.BooleanField(blank = True)
    # Used to indicate when the reading only applies to a subset of the related kanji objects.
    restrictions = models.TextField(blank = True)
    # General coded information pertaining to the specific reading typically used to indicate some unusual aspect of the reading.
    information = models.TextField(blank = True)
    # Eecords information about the relative priority of the entry, such as frequency and publications.
    priorities = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, con: {self.content}, nok: {self.no_kanji}, restr: {self.restrictions}, inf: {self.information}, pri: {self.priorities}'

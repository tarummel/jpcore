from django.contrib.postgres.fields import ArrayField
from django.db import models


# The kanji element, or in its absence, the reading element, is the defining component of each entry.
# The overwhelming majority of entries will have a single kanji element associated with a word in Japanese. 
# Where there are multiple kanji elements within an entry, they will be orthographical variants of the same word, 
# either using variations in okurigana, or alternative and equivalent kanji. 
# Common "mis-spellings" may be included, provided they are associated with appropriate information fields. 
# Synonyms are not included; they may be indicated in the cross-reference field associated with the sense element.
class JMdictKanji(models.Model):
    entry = models.ForeignKey('JMdictEntry', related_name = 'jkanji', on_delete = models.CASCADE)

    # A word or short phrase in Japanese which is written using at least one non-kana character (usually kanji, but can 
    # be other characters).
    content = models.TextField(blank = True)
    # Coded information field related specifically to the orthography of the keb and will typically indicate some 
    # unusual aspect, such as okurigana irregularity.
    information = models.TextField(blank = True)
    # Records information about the relative priority of the entry, such as frequency and publications.
    priorities = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'ent: {self.entry.ent_seq}, con: {self.content}, inf: {self.information}, pri: {self.priorities}'

from django.db import models


# Records the information about the source language(s) of a loan-word/gairaigo.
class JMdictSource(models.Model):
    sense = models.ForeignKey('JMdictSense', related_name = 'jsource', on_delete = models.CASCADE)

    # Value (if any) is the source word or phrase.
    content = models.TextField()
    # Defines the language(s) from which a loanword is drawn other than English.
    language = models.TextField(blank = True)
    # Indicates whether the lsource element fully or partially describes the source word or phrase of the loanword.
    partial = models.BooleanField(blank = True)
    # Indicates 'waseieigo', e.g. a word that appears English-like but either do not exist in English or have a different meaning.
    waseieigo = models.BooleanField(blank = True)

    def __str__(self):
        return f'ent: {self.sense.entry}, con: {self.content}, lang: {self.language}, part: {self.partial}, wasei: {self.waseieigo}'

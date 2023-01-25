from django.db import models

class JMdictSource(models.Model):
    sense = models.ForeignKey('JMdictSense', related_name = 'jsource', on_delete = models.CASCADE)

    content = models.TextField()
    language = models.TextField(blank = True)
    partial = models.BooleanField(blank = True)
    waseieigo = models.BooleanField(blank = True)

    def __str__(self):
        return f'ent: {self.sense.entry}, con: {self.content}, lang: {self.language}, part: {self.partial}, wasei: {self.waseieigo}'

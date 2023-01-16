from django.db import models

class JMdictSource(models.Model):
    sense = models.ForeignKey('JMdictSense', on_delete = models.CASCADE)

    content = models.TextField()
    language = models.TextField(blank = True)
    partial = models.BooleanField(blank = True)
    waseieigo = models.BooleanField(blank = True)

    def __str__(self):
        return f'id: {self.id}, ent: {self.sense.entry}, cont: {self.content}, lang: {self.language}, part: {self.partial}, wasei: {self.waseieigo}'

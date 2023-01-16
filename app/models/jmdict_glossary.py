from django.db import models

class JMdictGlossary(models.Model):
    sense = models.ForeignKey('JMdictSense', on_delete = models.CASCADE)

    gloss = models.TextField(blank = True)
    language = models.TextField(blank = True)
    type = models.TextField(blank = True)

    def __str__(self):
        return f' \
            entry: {self.sense.entry.ent_seq,}, \
            gloss: {self.gloss} \
            lang: {self.language} \
            type: {self.type} \
        '

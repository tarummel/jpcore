from django.db import models


# Within each sense will be one or more "glosses", i.e. target-language words or phrases which are equivalents to the Japanese word. 
# This element would normally be present, however it may be omitted in entries which are purely for a cross-reference.
class JMdictGlossary(models.Model):
    sense = models.ForeignKey('JMdictSense', related_name = 'jglossary', on_delete = models.CASCADE)

    # Translational element from Japanese, may be omitted in entries which are purely for a cross-reference.
    gloss = models.TextField(blank = True)
    # Defines the target language of the gloss.
    language = models.TextField(blank = True)
    # Specifies that the gloss is of a particular type, e.g. "lit" (literal), "fig" (figurative), "expl" (explanation).
    type = models.TextField(blank = True)

    def __str__(self):
        return f'ent: {self.sense.entry.ent_seq,}, glo: {self.gloss}, lang: {self.language}, type: {self.type}'

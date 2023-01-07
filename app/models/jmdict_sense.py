from django.db import models

class JMdictSense(models.Model):
    entry = models.ForeignKey('JMdictEntry', on_delete = models.CASCADE)

    # xreferences
    # antonyms
    # parts_of_speech
    # fields
    # misc
    # language_source
    # dialects
    # examples

    # def __str__(self):
    #     return "{}".format(
    #         self.id,
    #     )

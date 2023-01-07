from django.contrib.postgres.fields import ArrayField
from django.db import models

class JMdictKanji(models.Model):
    entry = models.ForeignKey('JMdictEntry', on_delete = models.CASCADE)

    element = models.TextField(blank = False)
    information = models.TextField(blank = True)
    priorities = ArrayField(models.CharField(blank = True, max_length = 8), size = 8)

    def __str__(self):
        return "{} {} {}".format(
            self.element,
            self.information,
            self.priorities,
        )
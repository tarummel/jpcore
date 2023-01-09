from django.db import models

class JMdictGlossary(models.Model):
    sense = models.ForeignKey('JMdictSense', on_delete = models.CASCADE)

    gloss = models.TextField(blank = True, null = True)
    # language = models.TextField(blank = True)
    # gender = models.TextField(blank = True)
    # type = models.TextField(blank = True)

    def __str__(self):
        return "{}".format(
            self.gloss,
            # self.language,
            # self.gender,
            # self.type,
        )
from django.db import models


# The codepoint element states the code of the character in the various character set standards.
class KDCodePoint(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdcodepoint')

    ucs = models.TextField(blank = True)
    jis208 = models.TextField(blank = True)
    jis212 = models.TextField(blank = True)
    jis213 = models.TextField(blank = True)
    
    def __str__(self):
        return f'ucs: {self.ucs}, jis208: {self.jis208}, jis212: {self.jis212}, jis213: {self.jis213}'

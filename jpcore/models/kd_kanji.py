from django.db import models

# Start of a KanjiDict entry
class KDKanji(models.Model):
    
    # The character itself in UTF8 coding.
    kanji = models.TextField()

    def __str__(self):
        return f'kanji: {self.kanji}'

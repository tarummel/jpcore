from django.db import models

# Start of a KanjiDic entry
class KDKanji(models.Model):
    
    # The character itself in UTF8 coding.
    kanji = models.TextField()
    
    # skipcode_set/skipcode = skip_codes reverse reference
    # visual

    def __str__(self):
        return f'kanji: {self.kanji}'

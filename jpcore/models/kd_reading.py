from django.contrib.postgres.fields import ArrayField
from django.db import models


# Contains the reading or pronunciation of the kanji.
class KDReading(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdreading')
    
    # the modern PinYin romanization of the Chinese reading of the kanji. The tones are represented by a concluding digit.
    ch_pinyin = ArrayField(models.TextField(), blank = True)

    # the romanized form of the Korean reading(s) of the kanji.
    ko_romanized = ArrayField(models.TextField(), blank = True)
    
    # the Korean reading(s) of the kanji in hangul.
    ko_hangul = ArrayField(models.TextField(), blank = True)

    # the Vietnamese readings supplied by Minh Chau Pham.
    vi_chu = ArrayField(models.TextField(), blank = True)

    # the "on" Japanese reading of the kanji based on Chinese pronunciation, in katakana.
    ja_on = ArrayField(models.TextField(), blank = True)

    # the "kun" Japanese reading of the kanji based on Japanese pronunciation, usually in hiragana.
    ja_kun = ArrayField(models.TextField(), blank = True)
    
    # Japanese readings that are now only associated with names.
    ja_nanori = ArrayField(models.TextField(), blank = True)

    def __str__(self):
        return f'onyomi: {self.ja_on}, kunyomi: {self.ja_kun}'

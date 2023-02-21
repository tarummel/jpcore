from django.test import TestCase
from jpcore.models import KDKanji, KDReading


class KDReadingTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        reading = KDReading.objects.create(
            kanji = kanji, 
            ch_pinyin = ['ji4'],
            ko_romanized = ['we'],
            ko_hangul = ['와'],
            vi_chu = ['Kế'],
            ja_on = ['ケイ'],
            ja_kun = ['うつく.しい'],
            ja_nanori = ['い']
        )
        saved = KDReading.objects.get(id = reading.id)
        
        self.assertEqual(saved.ch_pinyin, reading.ch_pinyin)
        self.assertEqual(saved.ko_romanized, reading.ko_romanized)
        self.assertEqual(saved.ko_hangul, reading.ko_hangul)
        self.assertEqual(saved.vi_chu, reading.vi_chu)
        self.assertEqual(saved.ja_on, reading.ja_on)
        self.assertEqual(saved.ja_kun, reading.ja_kun)
        self.assertEqual(saved.ja_nanori, reading.ja_nanori)

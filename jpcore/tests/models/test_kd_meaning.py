from django.test import TestCase
from jpcore.models import KDKanji, KDMeaning


class KDMeaningTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        meaning = KDMeaning.objects.create(
            kanji = kanji,
            en = ['test', 'test two']
        )
        saved = KDMeaning.objects.get(id = meaning.id)
        
        self.assertEqual(saved.en, meaning.en)

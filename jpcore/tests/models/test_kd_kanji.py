from django.test import TestCase
from jpcore.models import KDKanji


class KDKanjiTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        saved = KDKanji.objects.get(id = kanji.id)
        self.assertEqual(saved.kanji, kanji.kanji)

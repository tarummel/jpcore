from django.test import TestCase
from jpcore.models import KDKanji, KDRadical


class KDRadicalTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        rad = KDRadical.objects.create(kanji = kanji, classical = '1', nelson = '2')
        saved = KDRadical.objects.get(id = rad.id)
        
        self.assertEqual(saved.classical, rad.classical)
        self.assertEqual(saved.nelson, rad.nelson)

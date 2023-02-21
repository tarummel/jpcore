from django.test import TestCase
from jpcore.models import KDKanji, KDCodePoint


class KDCodePointTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        cp = KDCodePoint.objects.create(kanji = kanji, ucs = '1', jis208 = '2', jis212 = '3', jis213 = '4')
        saved = KDCodePoint.objects.get(id = cp.id)
        
        self.assertEqual(saved.ucs, cp.ucs)
        self.assertEqual(saved.jis208, cp.jis208)
        self.assertEqual(saved.jis212, cp.jis212)
        self.assertEqual(saved.jis213, cp.jis213)

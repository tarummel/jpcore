from django.test import TestCase
from jpcore.models import KDKanji, SkipCode


class RadicalTestCase(TestCase):

    def test_create(self):
        kanji1 = KDKanji.objects.create(
            kanji = '一'
        )
        kanji2 = KDKanji.objects.create(
            kanji = '二'
        )
        kanji3 = KDKanji.objects.create(
            kanji = '三'
        )
        skip1 = SkipCode.objects.create(
            category = 1,
            main = 2,
            sub = 3
        )
        skip2 = SkipCode.objects.create(
            category = 4,
            main = 5,
            sub = 6
        )
        skip3 = SkipCode.objects.create(
            category = 7,
            main = 8,
            sub = 9
        )
        
        skip1.kanji.set([kanji1])
        skip2.kanji.set([kanji1, kanji2])
        skip3.kanji.set([kanji1, kanji2, kanji3])

        savedKanji1 = KDKanji.objects.get(id = kanji1.id)
        savedKanji2 = KDKanji.objects.get(id = kanji2.id)
        savedKanji3 = KDKanji.objects.get(id = kanji3.id)
        savedSkip1 = SkipCode.objects.get(id = skip1.id)
        savedSkip2 = SkipCode.objects.get(id = skip2.id)
        savedSkip3 = SkipCode.objects.get(id = skip3.id)

        self.assertEqual(savedKanji1.kanji, kanji1.kanji)
        self.assertEqual(list(savedKanji1.skipcode_set.all()), [skip1, skip2, skip3])
        self.assertEqual(savedSkip1.category, skip1.category)
        self.assertEqual(savedSkip1.main, skip1.main)
        self.assertEqual(savedSkip1.sub, skip1.sub)
        self.assertEqual(list(savedSkip1.kanji.all()), [kanji1])

        self.assertEqual(savedKanji2.kanji, kanji2.kanji)
        self.assertEqual(list(savedKanji2.skipcode_set.all()), [skip2, skip3])
        self.assertEqual(savedSkip2.category, skip2.category)
        self.assertEqual(savedSkip2.main, skip2.main)
        self.assertEqual(savedSkip2.sub, skip2.sub)
        self.assertEqual(list(savedSkip2.kanji.all()), [kanji1, kanji2])

        self.assertEqual(savedKanji3.kanji, kanji3.kanji)
        self.assertEqual(list(savedKanji3.skipcode_set.all()), [skip3])
        self.assertEqual(savedSkip3.category, skip3.category)
        self.assertEqual(savedSkip3.main, skip3.main)
        self.assertEqual(savedSkip3.sub, skip3.sub)
        self.assertEqual(list(savedSkip3.kanji.all()), [kanji1, kanji2, kanji3])

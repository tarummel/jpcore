from django.test import TestCase
from app import models

class JMdictSenseTestCase(TestCase):
    k1rad1, k1rad2, k1rad3 = None, None, None
    k2rad1, k2rad2, k2rad3 = None, None, None 

    def setUp(self):
        self.k1rad1 = models.KanijRadical(id = 1, kanji = '亜', radical = '｜')
        self.k1rad2 = models.KanijRadical(id = 2, kanji = '亜', radical = '一')
        self.k1rad3 = models.KanijRadical(id = 3, kanji = '亜', radical = '口')
        self.k2rad1 = models.KanijRadical(id = 7, kanji = '以', radical = '｜')
        self.k2rad2 = models.KanijRadical(id = 8, kanji = '以', radical = '人')
        self.k2rad3 = models.KanijRadical(id = 9, kanji = '以', radical = '丶')

        self.k1rad1.save()
        self.k1rad2.save()
        self.k1rad3.save()
        self.k2rad1.save()
        self.k2rad2.save()
        self.k2rad3.save()

    def testCreate(self):
        nk1r1 = models.KanjiRadical.objects.get(id = self.k1rad1.id)
        nk1r2 = models.KanjiRadical.objects.get(id = self.k1rad2.id)
        nk1r3 = models.KanjiRadical.objects.get(id = self.k1rad3.id)
        nk2r1 = models.KanjiRadical.objects.get(id = self.k2rad1.id)
        nk2r2 = models.KanjiRadical.objects.get(id = self.k2rad2.id)
        nk2r3 = models.KanjiRadical.objects.get(id = self.k2rad3.id)

        self.assertEqual(nk1r1.id, self.k1rad1.id)
        self.assertEqual(nk1r1.kanji, self.k1rad1.kanji)
        self.assertEqual(nk1r1.radical, self.k1rad1.radical)
        
        self.assertEqual(nk1r2.id, self.k1rad2.id)
        self.assertEqual(nk1r2.kanji, self.k1rad2.kanji)
        self.assertEqual(nk1r2.radical, self.k1rad2.radical)

        self.assertEqual(nk1r3.id, self.k1rad3.id)
        self.assertEqual(nk1r3.kanji, self.k1rad3.kanji)
        self.assertEqual(nk1r3.radical, self.k1rad3.radical)

        self.assertEqual(nk2r1.id, self.k2rad1.id)
        self.assertEqual(nk2r1.kanji, self.k2rad1.kanji)
        self.assertEqual(nk2r1.radical, self.k2rad1.radical)

        self.assertEqual(nk2r2.id, self.k2rad2.id)
        self.assertEqual(nk2r2.kanji, self.k2rad2.kanji)
        self.assertEqual(nk2r2.radical, self.k2rad2.radical)

        self.assertEqual(nk2r3.id, self.k2rad3.id)
        self.assertEqual(nk2r3.kanji, self.k2rad3.kanji)
        self.assertEqual(nk2r3.radical, self.k2rad3.radical)

    def testGetByRadical(self):
        radks = models.KanjiRadical.objects.get(radical = self.k1rad1.radical).values_list('kanji', flat = True)

        self.assertEqual(len(radks), 2)
        self.assertTrue(self.k1rad1.kanji in radks)
        self.assertTrue(self.k2rad1.kanji in radks)



    def testGetByKanji(self):
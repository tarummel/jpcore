from django.test import TestCase
from jpcore.models import Radical, Kanji


class RadicalTestCase(TestCase):

    def test_create(self):
        savedRadical = Radical.objects.create(number = 147, radical = '見', strokes = 7, meaning = 'to see', reading = 'みる', frequency = 70, notes = '')

        radical = Radical.objects.get(id = savedRadical.id)

        self.assertEqual(radical.id, savedRadical.id)
        self.assertEqual(radical.radical, savedRadical.radical)
        self.assertEqual(radical.strokes, savedRadical.strokes)
        self.assertEqual(radical.meaning, savedRadical.meaning)
        self.assertEqual(radical.reading, savedRadical.reading)
        self.assertEqual(radical.frequency, savedRadical.frequency)
        self.assertEqual(radical.notes, savedRadical.notes)
        self.assertEqual(radical.kanji_set.all().count(), 0)

    def test_add_kanji(self):
        savedRad1 = Radical.objects.create(number = 147, radical = '見', strokes = 7, meaning = 'to see', reading = 'みる', frequency = 70, notes = '')
        savedRad2 = Radical.objects.create(number = 109, radical = '目', strokes = 5, meaning = 'eye', reading = 'め', frequency = 819, notes = '')
        savedRad3 = Radical.objects.create(number = 12, radical = '儿', strokes = 2, meaning = 'eight', reading = 'はちがしら', frequency = 1127, notes = '')

        self.assertEqual(savedRad1.kanji_set.all().count(), 0)
        self.assertEqual(savedRad2.kanji_set.all().count(), 0)
        self.assertEqual(savedRad3.kanji_set.all().count(), 0)

        savedKanji = Kanji.objects.create(kanji = '見', strokes = 7)
        savedRad1.kanji_set.add(savedKanji)
        savedRad2.kanji_set.add(savedKanji)
        savedRad3.kanji_set.add(savedKanji)

        rad1 = Radical.objects.get(id = savedRad1.id)
        rad2 = Radical.objects.get(id = savedRad2.id)
        rad3 = Radical.objects.get(id = savedRad3.id)

        self.assertEqual(rad1.kanji_set.all().count(), 1)
        self.assertEqual(rad2.kanji_set.all().count(), 1)
        self.assertEqual(rad3.kanji_set.all().count(), 1)

        kanji = Kanji.objects.get(id = savedKanji.id)

        rad1kanji = rad1.kanji_set.all()[0]
        self.assertEqual(rad1kanji.kanji, kanji.kanji)
        self.assertEqual(rad1kanji.strokes, kanji.strokes)
        
        rad2kanji = rad2.kanji_set.all()[0]
        self.assertEqual(rad2kanji.kanji, kanji.kanji)
        self.assertEqual(rad2kanji.strokes, kanji.strokes)
        
        rad3kanji = rad3.kanji_set.all()[0]
        self.assertEqual(rad3kanji.kanji, kanji.kanji)
        self.assertEqual(rad3kanji.strokes, kanji.strokes)

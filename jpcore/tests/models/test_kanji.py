from django.test import TestCase
from jpcore.models import Kanji, Radical

class KanjiTestCase(TestCase):

    def test_create(self):
        savedKanji = Kanji.objects.create(kanji = '心', strokes = 4)

        kanji = Kanji.objects.get(id = savedKanji.id)

        self.assertEqual(kanji.kanji, savedKanji.kanji)
        self.assertEqual(kanji.strokes, savedKanji.strokes)
        self.assertEqual(kanji.radicals.all().count(), 0)
        

    def test_add_radicals(self):
        savedKanji = Kanji.objects.create(kanji = '見', strokes = 7)
        
        savedRad1 = Radical.objects.create(number = 147, radical = '見', strokes = 7, meaning = 'to see', reading = 'みる', frequency = 70, notes = '')
        savedRad2 = Radical.objects.create(number = 109, radical = '目', strokes = 5, meaning = 'eye', reading = 'め', frequency = 819, notes = '')
        savedRad3 = Radical.objects.create(number = 12, radical = '儿', strokes = 2, meaning = 'eight', reading = 'はちがしら', frequency = 1127, notes = '')
        
        self.assertEqual(savedKanji.radicals.all().count(), 0)

        savedKanji.radicals.add(savedRad1)
        savedKanji.radicals.add(savedRad2)
        savedKanji.radicals.add(savedRad3)

        kanji = Kanji.objects.get(id = savedKanji.id)

        rad1 = Radical.objects.get(id = savedRad1.id)
        rad2 = Radical.objects.get(id = savedRad2.id)
        rad3 = Radical.objects.get(id = savedRad3.id)

        self.assertEqual(kanji.kanji, savedKanji.kanji)
        self.assertEqual(kanji.strokes, savedKanji.strokes)
        self.assertEqual(kanji.radicals.all().count(), 3)
        
        r1 = kanji.radicals.all()[0]
        self.assertEqual(r1.id, rad1.id)
        self.assertEqual(r1.radical, rad1.radical)
        self.assertEqual(r1.strokes, rad1.strokes)
        self.assertEqual(r1.meaning, rad1.meaning)
        self.assertEqual(r1.reading, rad1.reading)
        self.assertEqual(r1.frequency, rad1.frequency)
        self.assertEqual(r1.notes, rad1.notes)

        r2 = kanji.radicals.all()[1]
        self.assertEqual(r2.id, rad2.id)
        self.assertEqual(r2.radical, rad2.radical)
        self.assertEqual(r2.strokes, rad2.strokes)
        self.assertEqual(r2.meaning, rad2.meaning)
        self.assertEqual(r2.reading, rad2.reading)
        self.assertEqual(r2.frequency, rad2.frequency)
        self.assertEqual(r2.notes, rad2.notes)

        r3 = kanji.radicals.all()[2]
        self.assertEqual(r3.id, rad3.id)
        self.assertEqual(r3.radical, rad3.radical)
        self.assertEqual(r3.strokes, rad3.strokes)
        self.assertEqual(r3.meaning, rad3.meaning)
        self.assertEqual(r3.reading, rad3.reading)
        self.assertEqual(r3.frequency, rad3.frequency)
        self.assertEqual(r3.notes, rad3.notes)

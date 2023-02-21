from django.test import TestCase
from jpcore.models import KDKanji, KDMisc


class KDMiscTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        misc = KDMisc.objects.create(
            kanji = kanji,
            grade = '1',
            frequency = '25',
            strokes = '7',
            jlpt = '4',
            radical_names = ['けいがしら']
        )
        saved = KDMisc.objects.get(id = misc.id)
        
        self.assertEqual(saved.grade, misc.grade)
        self.assertEqual(saved.frequency, misc.frequency)
        self.assertEqual(saved.strokes, misc.strokes)
        self.assertEqual(saved.jlpt, misc.jlpt)
        self.assertEqual(saved.radical_names, misc.radical_names)

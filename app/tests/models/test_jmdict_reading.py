from django.test import TestCase
from app import models

class JMdictReadingTestCase(TestCase):
    oEntry, oReading = None, None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000010)
        self.oReading = models.JMdictReading.objects.create(
            id = 3,
            entry = self.oEntry,
            element = '明白', 
            no_kanji = True,
            restrictions = '彼',
            information = '&ok;', 
            priorities = ['ichi1'],
        )

    def test_create_and_update(self):
        cReading = models.JMdictReading.objects.get(id = self.oReading.id)

        self.assertEqual(cReading.element, self.oReading.element)
        self.assertEqual(cReading.no_kanji, self.oReading.no_kanji)
        self.assertEqual(cReading.restrictions, self.oReading.restrictions)
        self.assertEqual(cReading.information, self.oReading.information)
        self.assertEqual(cReading.priorities, self.oReading.priorities)

        cEntry = cReading.entry

        self.assertTrue(cEntry)
        self.assertEqual(cEntry.ent_seq, self.oEntry.ent_seq)

        cReading.element = ''
        cReading.no_kanji = False
        cReading.restrictions = ''
        cReading.information = ''
        cReading.priorities = ['ichi1', 'news1']
        cReading.save()

        nReading = models.JMdictReading.objects.get(id = cReading.id)

        self.assertTrue(nReading)
        self.assertEqual(nReading.element, cReading.element)
        self.assertEqual(nReading.no_kanji, cReading.no_kanji)
        self.assertEqual(nReading.restrictions, cReading.restrictions)
        self.assertEqual(nReading.information, cReading.information)
        self.assertEqual(nReading.priorities, cReading.priorities)


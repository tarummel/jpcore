from django.test import TestCase
from app import models

class JMdictKanjiTestCase(TestCase):
    oEntry, oKanji = None, None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000010)
        self.oKanji = models.JMdictKanji.objects.create(
            id = 7,
            entry = self.oEntry,
            element = '明白', 
            information = '&ateji;', 
            priorities = ['news1'],
        )

    def test_create_and_update(self):
        # Create
        cKanji = models.JMdictKanji.objects.get(id = self.oKanji.id)

        self.assertTrue(cKanji)
        self.assertEqual(cKanji.id, self.oKanji.id)
        self.assertEqual(cKanji.element, self.oKanji.element)
        self.assertEqual(cKanji.information, self.oKanji.information)
        self.assertEqual(cKanji.priorities, self.oKanji.priorities)

        cEntry = cKanji.entry

        self.assertTrue(cEntry)
        self.assertEqual(cEntry.ent_seq, self.oEntry.ent_seq)

        # Update
        cKanji.element = '〃'
        cKanji.information = '&rK;'
        cKanji.priorities = ['news1', 'ichi1']
        cKanji.save()

        nKanji = models.JMdictKanji.objects.get(id = self.oKanji.id)

        self.assertTrue(nKanji)
        self.assertEqual(nKanji.id, cKanji.id)
        self.assertEqual(nKanji.element, cKanji.element)
        self.assertEqual(nKanji.information, cKanji.information)
        self.assertEqual(nKanji.priorities, cKanji.priorities)
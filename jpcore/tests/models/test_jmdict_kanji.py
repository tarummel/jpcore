from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictKanji

class JMdictKanjiTestCase(TestCase):
    oEntry, oKanji = None, None

    def setUp(self):
        self.oEntry = JMdictEntry(ent_seq = 1000010)
        self.oKanji = JMdictKanji(
            id = 7,
            entry = self.oEntry,
            content = '明白', 
            information = '&ateji;', 
            priorities = ['news1'],
        )
        self.oEntry.save()
        self.oKanji.save()

    def testCreateAndUpdate(self):
        cKanji = JMdictKanji.objects.get(id = self.oKanji.id)

        self.assertTrue(cKanji)
        self.assertEqual(cKanji.id, self.oKanji.id)
        self.assertEqual(cKanji.content, self.oKanji.content)
        self.assertEqual(cKanji.information, self.oKanji.information)
        self.assertEqual(cKanji.priorities, self.oKanji.priorities)

        cEntry = cKanji.entry

        self.assertTrue(cEntry)
        self.assertEqual(cEntry.ent_seq, self.oEntry.ent_seq)

        cKanji.content = '〃'
        cKanji.information = '&rK;'
        cKanji.priorities = ['news1', 'ichi1']
        cKanji.save()

        nKanji = JMdictKanji.objects.get(id = self.oKanji.id)

        self.assertTrue(nKanji)
        self.assertEqual(nKanji.id, cKanji.id)
        self.assertEqual(nKanji.content, cKanji.content)
        self.assertEqual(nKanji.information, cKanji.information)
        self.assertEqual(nKanji.priorities, cKanji.priorities)

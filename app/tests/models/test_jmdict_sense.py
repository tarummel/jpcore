from django.test import TestCase
from app import models

class JMdictSenseTestCase(TestCase):
    oEntry, oSense = None, None

    def setUp(self):
        self.oEntry = models.JMdictEntry(ent_seq = 1000020)
        self.oSense = models.JMdictSense(
            id = 5, 
            entry = self.oEntry,
            xreferences = [],
            antonyms = [],
            parts_of_speech = [],
            fields = [],
            misc = [],
            dialects = [],
            information = ''
        )
        self.oEntry.save()
        self.oSense.save()

    def testCreateAndUpdate(self):
        nSense = models.JMdictSense.objects.get(id = self.oSense.id)

        self.assertTrue(nSense)
        # self.assertEqual(sense.xreferences, '')
        # self.assertEqual(sense.antonyms, '')
        # self.assertEqual(sense.parts_of_speech, '')
        # self.assertEqual(sense.fields, '')
        # self.assertEqual(sense.misc, '')
        # self.assertEqual(sense.language_source, '')
        # self.assertEqual(sense.dialects, '')
        # self.assertEqual(sense.examples, '')

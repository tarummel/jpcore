from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictSense

class JMdictSenseTestCase(TestCase):
    oEntry, oSense = None, None

    def setUp(self):
        self.oEntry = JMdictEntry(ent_seq = 1000020)
        self.oSense = JMdictSense(
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
        cSense = JMdictSense.objects.get(id = self.oSense.id)

        self.assertTrue(cSense)
        self.assertEqual(cSense.xreferences, self.oSense.xreferences)
        self.assertEqual(cSense.antonyms, self.oSense.antonyms)
        self.assertEqual(cSense.parts_of_speech, self.oSense.parts_of_speech)
        self.assertEqual(cSense.fields, self.oSense.fields)
        self.assertEqual(cSense.misc, self.oSense.misc)
        self.assertEqual(cSense.dialects, self.oSense.dialects)
        self.assertEqual(cSense.information, self.oSense.information)

        cSense.xreferences = ['これ・1']
        cSense.antonyms = ['それ・1']
        cSense.parts_of_speech = ['&pn;']
        cSense.fields = ['&food;']
        cSense.misc = ['&pol;']
        cSense.dialects = ['ktb;']
        cSense.information = 'used for something or someone close to the speaker, including the speaker himself'
        cSense.save()

        nSense = JMdictSense.objects.get(id = self.oSense.id)

        self.assertTrue(nSense)
        self.assertEqual(nSense.xreferences, cSense.xreferences)
        self.assertEqual(nSense.antonyms, cSense.antonyms)
        self.assertEqual(nSense.parts_of_speech, cSense.parts_of_speech)
        self.assertEqual(nSense.fields, cSense.fields)
        self.assertEqual(nSense.misc, cSense.misc)
        self.assertEqual(nSense.dialects, cSense.dialects)
        self.assertEqual(nSense.information, cSense.information)

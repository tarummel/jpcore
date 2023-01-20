from django.test import TestCase
from jpcore import models

class JMdictGlossaryTestCase(TestCase):
    oEntry, oSense, oGloss = None, None, None

    def setUp(self):
        self.oEntry = models.JMdictEntry(ent_seq = 1000010)
        self.oSense = models.JMdictSense(
            id = 20, 
            entry = self.oEntry,
            xreferences = [],
            antonyms = [],
            parts_of_speech = [],
            fields = [],
            misc = [],
            dialects = [],
            information = ''
        )
        self.oGloss = models.JMdictGlossary(
            id = 2, 
            sense = self.oSense, 
            gloss = 'NHK Symphony Orchestra',
            language = 'chi',
            type = 'part'
        )
        self.oEntry.save()
        self.oSense.save()
        self.oGloss.save()

    def testCreateAndUpdate(self):
        cGloss = models.JMdictGlossary.objects.get(id = self.oGloss.id)
        cSense = models.JMdictSense.objects.get(id = self.oSense.id)
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        self.assertEqual(cSense, self.oSense)
        self.assertEqual(cEntry, self.oEntry)

        self.assertEqual(cGloss.gloss, self.oGloss.gloss)
        self.assertEqual(cGloss.language, self.oGloss.language)
        self.assertEqual(cGloss.type, self.oGloss.type)

        cGloss.gloss = 'plastic wrap'
        cGloss.language = 'ger'
        cGloss.type = 'tm'
        cGloss.save()

        nGloss = models.JMdictGlossary.objects.get(id = self.oGloss.id)

        self.assertEqual(nGloss.id, cGloss.id)
        self.assertEqual(nGloss.gloss, cGloss.gloss)
        self.assertEqual(nGloss.language, cGloss.language)
        self.assertEqual(nGloss.type, cGloss.type)

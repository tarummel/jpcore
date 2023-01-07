from django.test import TestCase
from app import models

class JMdictGlossaryTestCase(TestCase):
    oEntry, oSense, oGloss = None, None, None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000010)
        self.oSense = models.JMdictSense.objects.create(id = 20, entry = self.oEntry)
        self.oGloss = models.JMdictGlossary.objects.create(
            id = 2, 
            sense = self.oSense, 
            gloss = 'NHK Symphony Orchestra'
        )

    def test_created(self):
        cGloss = models.JMdictGlossary.objects.get(id = self.oGloss.id)

        self.assertEqual(cGloss.gloss, self.oGloss.gloss)
        # self.assertEqual(glossary.language, 'fre')
        # self.assertEqual(glossary.gender, '')
        # self.assertEqual(glossary.type, 'expl')
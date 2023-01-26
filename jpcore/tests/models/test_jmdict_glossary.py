from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictSense, JMdictGlossary


class JMdictGlossaryTestCase(TestCase):

    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000010)
        self.sense = JMdictSense.objects.create(
            id = 20, 
            entry = self.entry,
            xreferences = ['知識人'],
            antonyms = ['ドライ・1'],
            parts_of_speech = ['adjective (keiyoushi)'],
            fields = ['linguistics'],
            misc = ['archaic'],
            dialects = ['Hokkaido-ben'],
            information = 'some info'
        )
        self.glossary = JMdictGlossary.objects.create(
            id = 2, 
            sense = self.sense, 
            gloss = 'NHK Symphony Orchestra',
            language = 'chi',
            type = 'part'
        )

    def test_create_update(self):
        savedGloss = JMdictGlossary.objects.get(id = self.glossary.id)
        savedSense = JMdictSense.objects.get(id = self.sense.id)
        savedEntry = JMdictEntry.objects.get(ent_seq = self.entry.ent_seq)

        self.assertEqual(savedSense, self.sense)
        self.assertEqual(savedEntry, self.entry)
        self.assertEqual(savedGloss.gloss, self.glossary.gloss)
        self.assertEqual(savedGloss.language, self.glossary.language)
        self.assertEqual(savedGloss.type, self.glossary.type)

        savedGloss.gloss = 'plastic wrap'
        savedGloss.language = 'ger'
        savedGloss.type = 'tm'
        savedGloss.save()

        gloss = JMdictGlossary.objects.get(id = self.glossary.id)

        self.assertEqual(gloss.id, savedGloss.id)
        self.assertEqual(gloss.gloss, savedGloss.gloss)
        self.assertEqual(gloss.language, savedGloss.language)
        self.assertEqual(gloss.type, savedGloss.type)

from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictSense


class JMdictSenseTestCase(TestCase):

    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000020)
        self.sense = JMdictSense.objects.create(
            id = 21, 
            entry = self.entry,
            xreferences = ['人'],
            antonyms = ['ド'],
            parts_of_speech = ['noun or verb acting prenominally'],
            fields = ['biochemistry'],
            misc = ['character'],
            dialects = ['Kansai-ben'],
            information = 'some other info'
        )

    def test_create_update(self):
        savedSense = JMdictSense.objects.get(id = self.sense.id)

        self.assertTrue(savedSense)
        self.assertEqual(savedSense.xreferences, self.sense.xreferences)
        self.assertEqual(savedSense.antonyms, self.sense.antonyms)
        self.assertEqual(savedSense.parts_of_speech, self.sense.parts_of_speech)
        self.assertEqual(savedSense.fields, self.sense.fields)
        self.assertEqual(savedSense.misc, self.sense.misc)
        self.assertEqual(savedSense.dialects, self.sense.dialects)
        self.assertEqual(savedSense.information, self.sense.information)

        savedSense.xreferences = ['これ・1']
        savedSense.antonyms = ['それ・1']
        savedSense.parts_of_speech = ['&pn;']
        savedSense.fields = ['&food;']
        savedSense.misc = ['&pol;']
        savedSense.dialects = ['ktb;']
        savedSense.information = 'used for something or someone close to the speaker, including the speaker himself'
        savedSense.save()

        sense = JMdictSense.objects.get(id = self.sense.id)

        self.assertEqual(sense.xreferences, savedSense.xreferences)
        self.assertEqual(sense.antonyms, savedSense.antonyms)
        self.assertEqual(sense.parts_of_speech, savedSense.parts_of_speech)
        self.assertEqual(sense.fields, savedSense.fields)
        self.assertEqual(sense.misc, savedSense.misc)
        self.assertEqual(sense.dialects, savedSense.dialects)
        self.assertEqual(sense.information, savedSense.information)

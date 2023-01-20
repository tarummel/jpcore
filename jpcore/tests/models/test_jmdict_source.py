from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictSense, JMdictSource

class JMdictSourceTestCase(TestCase):
    oEntry, oSense, oSource = None, None, None

    def setUp(self):
        self.oEntry = JMdictEntry(ent_seq = 1000500)
        self.oSense = JMdictSense(
            id = 100,
            entry = self.oEntry,
            xreferences = [],
            antonyms = [],
            parts_of_speech = [],
            fields = [],
            misc = [],
            dialects = [],
            information = ''
        )
        self.oSource = JMdictSource(
            id = 49,
            sense = self.oSense,
            content = 'bēngzi',
            language = 'chi',
            partial = False,
            waseieigo = False,
        )
        self.oEntry.save()
        self.oSense.save()
        self.oSource.save()

    def testCreateAndUpdate(self):
        cSource = JMdictSource.objects.get(id = self.oSource.id)
        cSense = JMdictSense.objects.get(id = self.oSense.id)
        cEntry = JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        self.assertEqual(cEntry, self.oEntry)
        self.assertEqual(cSense, self.oSense)

        self.assertEqual(cSource.id, self.oSource.id)
        self.assertEqual(cSource.content, self.oSource.content)
        self.assertEqual(cSource.language, self.oSource.language)
        self.assertEqual(cSource.partial, self.oSource.partial)
        self.assertEqual(cSource.waseieigo, self.oSource.waseieigo)

        cSource.content = 'art déco'
        cSource.language = 'fre'
        cSource.partial = True
        cSource.waseieigo = True
        cSource.save()

        nSource = JMdictSource.objects.get(id = self.oSource.id)

        self.assertEqual(nSource.id, cSource.id)
        self.assertEqual(nSource.content, cSource.content)
        self.assertEqual(nSource.language, cSource.language)
        self.assertEqual(nSource.partial, cSource.partial)
        self.assertEqual(nSource.waseieigo, cSource.waseieigo)

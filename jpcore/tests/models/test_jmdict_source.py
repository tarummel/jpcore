from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictSense, JMdictSource


class JMdictSourceTestCase(TestCase):

    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000500)
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
        self.oSource = JMdictSource.objects.create(
            id = 49,
            sense = self.sense,
            content = 'bēngzi',
            language = 'chi',
            partial = False,
            waseieigo = False,
        )

    def test_create_update(self):
        savedSource = JMdictSource.objects.get(id = self.oSource.id)
        savedSense = JMdictSense.objects.get(id = self.sense.id)
        savedEntry = JMdictEntry.objects.get(ent_seq = self.entry.ent_seq)

        self.assertEqual(savedEntry, self.entry)
        self.assertEqual(savedSense, self.sense)

        self.assertEqual(savedSource.id, self.oSource.id)
        self.assertEqual(savedSource.content, self.oSource.content)
        self.assertEqual(savedSource.language, self.oSource.language)
        self.assertEqual(savedSource.partial, self.oSource.partial)
        self.assertEqual(savedSource.waseieigo, self.oSource.waseieigo)

        savedSource.content = 'art déco'
        savedSource.language = 'fre'
        savedSource.partial = True
        savedSource.waseieigo = True
        savedSource.save()

        source = JMdictSource.objects.get(id = self.oSource.id)

        self.assertEqual(source.id, savedSource.id)
        self.assertEqual(source.content, savedSource.content)
        self.assertEqual(source.language, savedSource.language)
        self.assertEqual(source.partial, savedSource.partial)
        self.assertEqual(source.waseieigo, savedSource.waseieigo)

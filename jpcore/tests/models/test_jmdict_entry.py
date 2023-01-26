from django.test import TestCase
from jpcore.models import JMdictEntry


class JMdictEntryTestCase(TestCase):

    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000000)

    def test_create(self):
        cEntry = JMdictEntry.objects.get(ent_seq = self.entry.ent_seq)
        self.assertEqual(cEntry, self.entry)

    def test_uneditable(self):
        savedEntry = JMdictEntry.objects.get(ent_seq = self.entry.ent_seq)

        savedEntry.ent_seq = 99999999
        savedEntry.save()

        entry = JMdictEntry.objects.get(ent_seq = self.entry.ent_seq)

        self.assertNotEqual(entry, savedEntry)
        self.assertEqual(entry, self.entry)

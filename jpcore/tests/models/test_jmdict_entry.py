from django.test import TestCase
from jpcore import models

class JMdictEntryTestCase(TestCase):
    oEntry = None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000000)
        self.oEntry.save()

    def testCreate(self):
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)
        self.assertEqual(cEntry, self.oEntry)

    def testUneditable(self):
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        cEntry.ent_seq = 99999999
        cEntry.save()

        nEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        self.assertNotEqual(nEntry, cEntry)
        self.assertEqual(nEntry, self.oEntry)

from django.test import TestCase
from app import models

class JMdictEntryTestCase(TestCase):
    oEntry = None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000000)

    def test_create(self):
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)
        self.assertEqual(cEntry, self.oEntry)

    def test_uneditable(self):
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        cEntry.ent_seq = 99999999
        cEntry.save()

        nEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)

        self.assertNotEqual(nEntry, cEntry)
        self.assertEqual(nEntry, self.oEntry)

            
            
        
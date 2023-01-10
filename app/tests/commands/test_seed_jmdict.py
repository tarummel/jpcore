from django.test import TestCase
from app import models

class SeedJMdictCommandTestCase(TestCase):
    oEntry = None

    def setUp(self):
        self.oEntry = models.JMdictEntry.objects.create(ent_seq = 1000000)

    def test_(self):
        cEntry = models.JMdictEntry.objects.get(ent_seq = self.oEntry.ent_seq)
        self.assertEqual(cEntry, self.oEntry)
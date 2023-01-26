from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictReading


class JMdictReadingTestCase(TestCase):

    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000010)
        self.reading = JMdictReading.objects.create(
            id = 3,
            entry = self.entry,
            content = '明白', 
            no_kanji = True,
            restrictions = '彼',
            information = '&ok;', 
            priorities = ['ichi1'],
        )

    def test_create_update(self):
        savedReading = JMdictReading.objects.get(id = self.reading.id)

        self.assertEqual(savedReading.entry.ent_seq, self.entry.ent_seq)
        self.assertEqual(savedReading.content, self.reading.content)
        self.assertEqual(savedReading.no_kanji, self.reading.no_kanji)
        self.assertEqual(savedReading.restrictions, self.reading.restrictions)
        self.assertEqual(savedReading.information, self.reading.information)
        self.assertEqual(savedReading.priorities, self.reading.priorities)

        savedReading.content = ''
        savedReading.no_kanji = False
        savedReading.restrictions = ''
        savedReading.information = ''
        savedReading.priorities = ['ichi1', 'news1']
        savedReading.save()

        reading = JMdictReading.objects.get(id = savedReading.id)

        self.assertEqual(reading.content, savedReading.content)
        self.assertEqual(reading.no_kanji, savedReading.no_kanji)
        self.assertEqual(reading.restrictions, savedReading.restrictions)
        self.assertEqual(reading.information, savedReading.information)
        self.assertEqual(reading.priorities, savedReading.priorities)

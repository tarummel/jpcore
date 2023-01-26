from django.test import TestCase
from jpcore.models import JMdictEntry, JMdictKanji


class JMdictKanjiTestCase(TestCase):
    
    def setUp(self):
        self.entry = JMdictEntry.objects.create(ent_seq = 1000010)
        self.kanji = JMdictKanji.objects.create(
            id = 7,
            entry = self.entry,
            content = '明白', 
            information = '&ateji;', 
            priorities = ['news1'],
        )

    def test_create_update(self):
        savedKanji = JMdictKanji.objects.get(id = self.kanji.id)

        self.assertEqual(savedKanji.entry.ent_seq, self.entry.ent_seq)
        self.assertEqual(savedKanji.id, self.kanji.id)
        self.assertEqual(savedKanji.content, self.kanji.content)
        self.assertEqual(savedKanji.information, self.kanji.information)
        self.assertEqual(savedKanji.priorities, self.kanji.priorities)

        savedKanji.content = '〃'
        savedKanji.information = '&rK;'
        savedKanji.priorities = ['news1', 'ichi1']
        savedKanji.save()

        kanji = JMdictKanji.objects.get(id = self.kanji.id)

        self.assertEqual(kanji.id, savedKanji.id)
        self.assertEqual(kanji.content, savedKanji.content)
        self.assertEqual(kanji.information, savedKanji.information)
        self.assertEqual(kanji.priorities, savedKanji.priorities)

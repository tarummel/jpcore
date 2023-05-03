from django.test import TestCase

from jpcore.models import KDKanji, VisualCloseness
from jpcore.management.helpers import SeedVisualClosenessHelper as helper

class SeedVisualClosenessHelperTestCase(TestCase):
    helper = helper()

    def setUp(self):
        self.kanji = KDKanji.objects.create(kanji = '葵')

    def test_parseLine(self):
        kanji = '凡'
        related = ['丸', '0.666667', '夕', '0.666667', '勺', '0.666667', '太', '0.5', '公', '0.5', '不', '0.5', '犬', '0.5', '帆', '0.5', '仏', '0.5', '丹', '0.5']
        # 凡 丸 0.666667 夕 0.666667 勺 0.666667 太 0.5 公 0.5 不 0.5 犬 0.5 帆 0.5 仏 0.5 丹 0.5
        input = f'{kanji} {" ".join(related)}'
        left, right = self.helper.parseLine(input)

        self.assertEqual(left, kanji)
        self.assertEqual(right, related)

    def test_getKDKanji(self):
        savedKanji = self.helper.getKDKanji(self.kanji.kanji)
        self.assertEqual(savedKanji, self.kanji)

    def test_getKDKanji_cache(self):
        cachedKanji = KDKanji(kanji = '夕')
        self.helper.kanjiCache[cachedKanji.kanji] = cachedKanji
        savedKanji = self.helper.getKDKanji(cachedKanji.kanji)
        self.assertEqual(savedKanji, cachedKanji)

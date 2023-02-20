from django.test import TestCase
from xml.etree import ElementTree as etree

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning
from jpcore.management.helpers import SeedKanjiDictHelper as helper

class SeedKanjiDictHelperTestCase(TestCase):
    helper = helper()

    def test_get_text(self):
        text = 'test'
        xml = etree.XML(f'<literal>{text}</literal>')

        value = self.helper.getText(xml, 'literal')

        self.assertEqual(value, text)

    def test_get_text_special_chars(self):
        text = '亜'
        xml = etree.XML(f'<literal>{text}</literal>')

        value = self.helper.getText(xml, 'literal')

        self.assertEqual(value, text)

    def test_get_text_by_attr(self):
        # text = '亜'
        text = 'test'
        xml = etree.XML(f'<codepoint><cp_value cp_type="ucs">{text}</cp_value></codepoint>')

        value = self.helper.getText(xml, 'cp_value')

        self.assertEqual(value, text)

    # def test_save_kanji(self):
    #     text = '亜'
    #     xml = etree.XML(f'<character><literal>{text}<literal></character>')

    #     kanji = self.helper.buildAndSaveKanji(xml)
    #     self.assertEqual(kanji.kanji, text)

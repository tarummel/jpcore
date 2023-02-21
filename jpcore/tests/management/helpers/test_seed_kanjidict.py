from django.test import TestCase
from lxml import etree

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning
from jpcore.management.helpers import SeedKanjiDictHelper as helper

class SeedKanjiDictHelperTestCase(TestCase):
    helper = helper()

    def setUp(self):
        self.kanji = KDKanji.objects.create(
            kanji = '葵'
        )

    def test_get_text(self):
        text = 'test'
        xml = etree.XML(f'<character><literal>{text}</literal></character>')

        value = self.helper.getText(xml, 'literal')

        self.assertEqual(value, text)

    def test_get_text_special_chars(self):
        text = '亜'
        xml = etree.XML(f'<character><literal>{text}</literal></character>')

        value = self.helper.getText(xml, 'literal')

        self.assertEqual(value, text)

    def test_get_text_by_attr(self):
        text = '亜'
        xml = etree.XML(f'<codepoint><cp_value cp_type="ucs">{text}</cp_value></codepoint>')

        value = self.helper.getText(xml, 'cp_value[@cp_type="ucs"]')

        self.assertEqual(value, text)

    def test_get_list(self):
        rn1, rn2 = 'しんよう','じゅうまた'
        xml = etree.XML(f'<misc><rad_name>{rn1}</rad_name><rad_name>{rn2}</rad_name></misc>')

        radical_names = self.helper.getList(xml, 'rad_name')
        self.assertEqual(radical_names, [rn1, rn2])

    def test_save_kanji(self):
        text = '亜'
        xml = etree.XML(f'<character><literal>{text}</literal></character>')

        kanji = self.helper.buildAndSaveKanji(xml)
        self.assertEqual(kanji.kanji, text)

    def test_save_codepoint(self):
        cp1, cp2 = '4e9c', '1-16-01'
        xml = etree.XML(f'<codepoint><cp_value cp_type="ucs">{cp1}</cp_value><cp_value cp_type="jis208">{cp2}</cp_value></codepoint>')

        codepoint = self.helper.buildAndSaveCodePoint(xml, self.kanji)
        self.assertEqual(codepoint.ucs, cp1)
        self.assertEqual(codepoint.jis208, cp2)

    def test_save_radical(self):
        r1, r2 = '61', '1'
        xml = etree.XML(f'<radical><rad_value rad_type="classical">{r1}</rad_value><rad_value rad_type="nelson_c">{r2}</rad_value></radical>')

        radical = self.helper.buildAndSaveRadical(xml, self.kanji)
        self.assertEqual(radical.classical, r1)
        self.assertEqual(radical.nelson, r2)

    def test_save_misc(self):
        grade, strokes, freq, rn1, rn2, jltp = '5', '4', '159', 'しんよう','じゅうまた', '2'
        xml = etree.XML(f'<misc><grade>{grade}</grade><stroke_count>{strokes}</stroke_count><freq>{freq}</freq><rad_name>{rn1}</rad_name><rad_name>{rn2}</rad_name><jlpt>{jltp}</jlpt></misc>')

        misc = self.helper.buildAndSaveMisc(xml, self.kanji)
        self.assertEqual(misc.grade, grade)
        self.assertEqual(misc.strokes, strokes)
        self.assertEqual(misc.frequency, freq)
        self.assertEqual(misc.radical_names, [rn1, rn2])
        self.assertEqual(misc.jlpt, jltp)

    def test_save_variant(self):
        v1, v2 = '3634', '2k4.6'
        xml = etree.XML(f'<misc><stroke_count>25</stroke_count><variant var_type="nelson_c">{v1}</variant><variant var_type="s_h">{v2}</variant></misc>')

        variants = self.helper.buildAndSaveVariant(xml, self.kanji)
        self.assertEqual(variants.nelson_c, v1)
        self.assertEqual(variants.sh, v2)

    def test_save_index(self):
        bp, moro, moroV, moroP = '2964', '3746', '2', '1066'
        xml = etree.XML(f'<dic_number><dic_ref dr_type="busy_people">{bp}</dic_ref><dic_ref dr_type="moro" m_vol="{moroV}" m_page="{moroP}">{moro}</dic_ref></dic_number>')

        index = self.helper.buildAndSaveIndex(xml, self.kanji)
        self.assertEqual(index.busy_people, bp)
        self.assertEqual(index.moro, moro)
        self.assertEqual(index.moro_volume, moroV)
        self.assertEqual(index.moro_page, moroP)

    def test_save_querycode(self):
        skip, sh_desc, four, deroo, ms1, ms2, ms3, ms4 = '2-3-4', '3p4.2', '4071.2', '1456', '2-3-6', '2-4-11', '2-3-10', '2-4-8'
        xml = etree.XML(f'<query_code><q_code qc_type="skip">{skip}</q_code><q_code qc_type="sh_desc">{sh_desc}</q_code><q_code qc_type="four_corner">{four}</q_code><q_code qc_type="deroo">{deroo}</q_code><q_code qc_type="skip" skip_misclass="posn">{ms1}</q_code><q_code qc_type="skip" skip_misclass="stroke_count">{ms2}</q_code><q_code qc_type="skip" skip_misclass="stroke_diff">{ms3}</q_code><q_code qc_type="skip" skip_misclass="stroke_and_posn">{ms4}</q_code></query_code>')

        qc = self.helper.buildAndSaveQueryCode(xml, self.kanji)
        self.assertEqual(qc.skip, skip)
        self.assertEqual(qc.sh_descriptor, sh_desc)
        self.assertEqual(qc.four_corner, four)
        self.assertEqual(qc.deroo, deroo)
        self.assertEqual(qc.misclass_pos, ms1)
        self.assertEqual(qc.misclass_strokes, ms2)
        self.assertEqual(qc.misclass_strokes_diff, ms3)
        self.assertEqual(qc.misclass_strokes_pos, ms4)

    def test_save_reading(self):
        pinyin, k_r, k_h, vt, ja_on, ja_kun, nanori = 'si4', 'sa', '사', 'Tự', 'シ', 'か.う', 'かい'
        xml = etree.XML(f'<reading_meaning><rmgroup><reading r_type="pinyin">{pinyin}</reading><reading r_type="korean_r">{k_r}</reading><reading r_type="korean_h">{k_h}</reading><reading r_type="vietnam">{vt}</reading><reading r_type="ja_on">{ja_on}</reading><reading r_type="ja_kun">{ja_kun}</reading></rmgroup><nanori>{nanori}</nanori></reading_meaning>')

        reading = self.helper.buildAndSaveReading(xml, self.kanji)
        self.assertEqual(reading.ch_pinyin, [pinyin])
        self.assertEqual(reading.ko_romanized, [k_r])
        self.assertEqual(reading.ko_hangul, [k_h])
        self.assertEqual(reading.vi_chu, [vt])
        self.assertEqual(reading.ja_on, [ja_on])
        self.assertEqual(reading.ja_kun, [ja_kun])
        self.assertEqual(reading.ja_nanori, [nanori])

    def test_save_meaning(self):
        m1, m2 = 'feminine', 'female'
        xml = etree.XML(f'<rmgroup><meaning>{m1}</meaning><meaning>{m2}</meaning><meaning m_lang="fr">femelle</meaning></rmgroup>')

        meaning = self.helper.buildAndSaveMeaning(xml, self.kanji)
        self.assertEqual(meaning.en, [m1, m2])

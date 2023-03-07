from django.test import TestCase
from lxml import etree

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning, SkipCode
from jpcore.management.helpers import SeedKanjiDicHelper as helper

class SeedKanjiDicHelperTestCase(TestCase):
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
        skip, sh_desc, four, deroo, ms1, ms2, ms3, ms4 = '2-3-4', '3p4.2', '4071.2', '1456', ['2-3-6'], ['2-4-11'], ['2-3-10'], ['2-4-8']
        xml = etree.XML(f'<query_code><q_code qc_type="skip">{skip}</q_code><q_code qc_type="sh_desc">{sh_desc}</q_code><q_code qc_type="four_corner">{four}</q_code><q_code qc_type="deroo">{deroo}</q_code><q_code qc_type="skip" skip_misclass="posn">{ms1[0]}</q_code><q_code qc_type="skip" skip_misclass="stroke_count">{ms2[0]}</q_code><q_code qc_type="skip" skip_misclass="stroke_diff">{ms3[0]}</q_code><q_code qc_type="skip" skip_misclass="stroke_and_posn">{ms4[0]}</q_code></query_code>')

        qc = self.helper.buildAndSaveQueryCode(xml, self.kanji)
        self.assertEqual(qc.skip, skip)
        self.assertEqual(qc.sh_descriptor, sh_desc)
        self.assertEqual(qc.four_corner, four)
        self.assertEqual(qc.deroo, deroo)
        self.assertEqual(qc.misclass_pos, ms1)
        self.assertEqual(qc.misclass_strokes, ms2)
        self.assertEqual(qc.misclass_strokes_diff, ms3)
        self.assertEqual(qc.misclass_strokes_pos, ms4)

    def test_handle_skipcodes(self):
        kanji = KDKanji.objects.create(
            kanji = '以'
        )
        qcode = KDQueryCode.objects.create(
            kanji = kanji,
            skip = '1-1-1',
            sh_descriptor = '4i10.1',
            four_corner = '2024.7',
            deroo = '2067',
            misclass_pos = ['3-12-1'],
            misclass_strokes = ['1-2-3'],
            misclass_strokes_diff = ['2-3-4', '4-1-1'],
            misclass_strokes_pos = ['1-2-3'] # dupe
        )

        skipcodes = self.helper.handleSkipCodes(qcode, kanji)
        
        savedKanji = KDKanji.objects.get(id = kanji.id)
        self.assertEqual(savedKanji.kanji, kanji.kanji)
        self.assertEqual(len(savedKanji.skipcode_set.all()), 5)
        
        key1 = qcode.skip.split('-')
        key2 = qcode.misclass_pos[0].split('-')
        key3 = qcode.misclass_strokes[0].split('-')
        key4 = qcode.misclass_strokes_diff[0].split('-')
        key5 = qcode.misclass_strokes_diff[1].split('-')

        skip1 = SkipCode.objects.get(category = key1[0], main = key1[1], sub = key1[2])
        skip2 = SkipCode.objects.get(category = key2[0], main = key2[1], sub = key2[2])
        skip3 = SkipCode.objects.get(category = key3[0], main = key3[1], sub = key3[2])
        skip4 = SkipCode.objects.get(category = key4[0], main = key4[1], sub = key4[2])
        skip5 = SkipCode.objects.get(category = key5[0], main = key5[1], sub = key5[2])

        self.assertEqual(savedKanji.skipcode_set.all()[0], skip1)
        self.assertEqual(savedKanji.skipcode_set.all()[1], skip2)
        self.assertEqual(savedKanji.skipcode_set.all()[2], skip3)
        self.assertEqual(savedKanji.skipcode_set.all()[3], skip4)
        self.assertEqual(savedKanji.skipcode_set.all()[4], skip5)

    def test_save_skipcode(self):
        kanji = KDKanji.objects.create(
            kanji = '以'
        )
        key = '1-2-3'
        values = key.split('-')
        skipcode = self.helper.buildAndSaveSkipCode(key, kanji)

        self.assertEqual(skipcode.category, values[0])
        self.assertEqual(skipcode.main, values[1])
        self.assertEqual(skipcode.sub, values[2])
        self.assertEqual(list(skipcode.kanji.all()), [kanji])

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

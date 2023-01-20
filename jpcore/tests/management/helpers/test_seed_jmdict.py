from django.test import TestCase
from xml.etree import ElementTree as etree

from jpcore.models import JMdictEntry, JMdictKanji, JMdictReading, JMdictSense, JMdictGlossary, JMdictSource
from jpcore.management.helpers import SeedJMdictHelper as helper

class SeedJMdictHelperTestCase(TestCase):
    helper = helper()

    def test_get_attributes_text(self):
        text = 'good morning'
        xml = etree.XML(f'<lsource>{text}</lsource>')

        value, attr = self.helper.getTextWithAttributes(xml)

        self.assertEqual(value, text)
        self.assertEqual(len(attr), 0)

    def test_get_attributes_text_with_kanji(self):
        text = '彼の人'
        xml = etree.XML(f'<gloss>{text}</gloss>')

        value, attr = self.helper.getTextWithAttributes(xml)
        
        self.assertEqual(value, text)
        self.assertEqual(len(attr), 0)

    def test_get_lsource_attributes(self):
        # xml: namespace should be removed
        lang = 'lang'

        text = 'unmoral'
        names = ['xml:lang', 'ls_type', 'ls_wasei']
        values = ['eng', 'part', 'y']
        xml = etree.XML(f'<lsource {names[0]}="{values[0]}" {names[1]}="{values[1]}" {names[2]}="{values[2]}">{text}</lsource>')

        value, attr = self.helper.getTextWithAttributes(xml)
        
        self.assertEqual(value, text)
        self.assertTrue(lang in attr)
        self.assertTrue(names[1] in attr)
        self.assertTrue(names[2] in attr)
        self.assertEqual(attr[lang], values[0])
        self.assertEqual(attr[names[1]], values[1])
        self.assertEqual(attr[names[2]], values[2])

    def test_get_gloss_attributes(self):
        # xml: namespace should be removed
        lang = 'lang'
        
        text = '彼の人'
        names = ['xml:lang', 'g_type']
        values = ['eng', 'expl']
        xml = etree.XML(f'<gloss {names[0]}="{values[0]}" {names[1]}="{values[1]}">{text}</gloss>')

        value, attr = self.helper.getTextWithAttributes(xml)
        
        self.assertEqual(value, text)
        self.assertTrue(lang in attr) 
        self.assertTrue(names[1] in attr)
        self.assertEqual(attr[lang], values[0])
        self.assertEqual(attr[names[1]], values[1])

    def test_get_text(self):
        text = 'Romanji'
        xml = etree.XML(f'<k_ele><keb>{text}</keb></k_ele>')

        value = self.helper.getText(xml, 'keb')

        self.assertEqual(value, text)

    def test_get_text_with_kanji(self):
        text = '護美箱'
        xml = etree.XML(f'<k_ele><keb>{text}</keb></k_ele>')

        value = self.helper.getText(xml, 'keb')

        self.assertEqual(value, text)

    def test_get_text_empty(self):
        xml = etree.XML(f'<k_ele></k_ele>')

        value = self.helper.getText(xml, 'keb')

        self.assertEqual(value, '')

    def test_get_list_one(self):
        text = 'shift'
        xml = etree.XML(f'<sense><gloss>{text}</gloss></sense>')

        values = self.helper.getList(xml, 'gloss')

        self.assertEqual(len(values), 1)
        self.assertEqual(values[0], text)


    def test_get_list_multiple(self):
        pos = ['adv', 'adv-to', 'vs']
        xml = etree.XML(f'<sense><pos>{pos[0]}</pos><pos>{pos[1]}</pos><pos>{pos[2]}</pos></sense>')

        values = self.helper.getList(xml, 'pos')

        self.assertEqual(len(values), 3)
        self.assertEqual(values[0], pos[0])
        self.assertEqual(values[1], pos[1])
        self.assertEqual(values[2], pos[2])

    def test_get_list_none(self):
        xml = etree.XML(f'<sense></sense>')

        values = self.helper.getList(xml, 'pos')

        self.assertEqual(values, [])

    def test_build_entry(self):
        seq = 12345678
        xml = etree.XML(f'<entry><ent_seq>{seq}</ent_seq></entry>')

        self.helper.buildAndSaveEntry(xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)

        self.assertEqual(savedEntry.ent_seq, seq)
    
    def test_build_kanji(self):
        seq = 1000000
        entry = JMdictEntry(ent_seq = seq)
        entry.save()

        keb, inf, pri = 'お凸', 'rK', ['ichi1', 'ichi2']
        xml = etree.XML(f'<k_ele><keb>{keb}</keb><ke_inf>{inf}</ke_inf><ke_pri>{pri[0]}</ke_pri><ke_pri>{pri[1]}</ke_pri></k_ele>')

        kanji = self.helper.buildAndSaveKanji(entry, xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)
        savedKanji = JMdictKanji.objects.get(id = kanji.id)

        self.assertEqual(savedEntry.ent_seq, seq)
        self.assertEqual(savedKanji.entry, savedEntry)
        self.assertEqual(savedKanji.content, keb)
        self.assertEqual(savedKanji.information, inf)
        self.assertEqual(savedKanji.priorities, pri)

    def test_build_reading(self):
        seq = 1000001
        entry = JMdictEntry(ent_seq = seq)
        entry.save()

        reb, inf, restr, pri = 'シーディープレーヤー', 'ok', 'ＣＤプレーヤー', ['spec1', 'news1']
        xml = etree.XML(f'<r_ele><reb>{reb}</reb><re_nokanji/><re_inf>{inf}</re_inf><re_restr>{restr}</re_restr><re_pri>{pri[0]}</re_pri><re_pri>{pri[1]}</re_pri></r_ele>')

        reading = self.helper.buildAndSaveReading(entry, xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)
        savedReading = JMdictReading.objects.get(id = reading.id)

        self.assertEqual(savedEntry.ent_seq, seq)
        self.assertEqual(savedReading.entry, savedEntry)
        self.assertEqual(savedReading.content, reb)
        self.assertEqual(savedReading.no_kanji, True)
        self.assertEqual(savedReading.restrictions, restr)
        self.assertEqual(savedReading.priorities, pri)

    def test_build_sense(self):
        seq = 1000002
        entry = JMdictEntry(ent_seq = seq)
        entry.save()

        pos = ['exp', 'unc']
        xref = ['うずら豆', 'お先に失礼します']
        ant = ['有段者', '情弱'] 
        misc = ['chem', 'food']
        field = ['abbr', 'pol'] 
        dial = ['hob', 'thb']
        inf = 'zero'
        xml = etree.XML(f'<sense><pos>{pos[0]}</pos><pos>{pos[1]}</pos><xref>{xref[0]}</xref><xref>{xref[1]}</xref><ant>{ant[0]}</ant><ant>{ant[1]}</ant><misc>{misc[0]}</misc><misc>{misc[1]}</misc><field>{field[0]}</field><field>{field[1]}</field><dial>{dial[0]}</dial><dial>{dial[1]}</dial><s_inf>{inf}</s_inf></sense>')

        sense = self.helper.buildAndSaveSense(entry, xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)
        savedSense = JMdictSense.objects.get(id = sense.id)

        self.assertEqual(savedEntry.ent_seq, seq)
        self.assertEqual(savedSense.entry, savedEntry)
        self.assertEqual(savedSense.parts_of_speech, pos)
        self.assertEqual(savedSense.xreferences, xref)
        self.assertEqual(savedSense.antonyms, ant)
        self.assertEqual(savedSense.misc, misc)
        self.assertEqual(savedSense.fields, field)
        self.assertEqual(savedSense.dialects, dial)
        self.assertEqual(savedSense.information, inf)

    def test_build_glossary(self):
        seq = 1000003
        entry = JMdictEntry(ent_seq = seq)
        entry.save()

        sense = JMdictSense(
            entry = entry,
            xreferences = [],
            antonyms = [],
            parts_of_speech = [],
            fields = [],
            misc = [],
            dialects = [],
            information = ''
        )
        sense.save()

        gloss, lang, type = '人', 'fre', 'lit'
        xml = etree.XML(f'<gloss xml:lang="{lang}" g_type="{type}">{gloss}</gloss>')

        glossary = self.helper.buildAndSaveGlossary(sense, xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)
        savedSense = JMdictSense.objects.get(id = sense.id)
        savedGlossary = JMdictGlossary.objects.get(id = glossary.id)

        self.assertEqual(savedEntry.ent_seq, seq)
        self.assertEqual(savedSense.entry, savedEntry)
        self.assertEqual(savedGlossary.sense, savedSense)
        self.assertEqual(savedGlossary.gloss, gloss)
        self.assertEqual(savedGlossary.language, lang)
        self.assertEqual(savedGlossary.type, type)

    def test_build_lsource(self):
        seq = 1000004
        entry = JMdictEntry(ent_seq = seq)
        entry.save()

        sense = JMdictSense(
            entry = entry,
            xreferences = [],
            antonyms = [],
            parts_of_speech = [],
            fields = [],
            misc = [],
            dialects = [],
            information = ''
        )
        sense.save()

        text, lang, type, wasei = 'occasionally', 'eng', 'part', 'y'
        xml = etree.XML(f'<lsource xml:lang="{lang}" ls_type="{type}" ls_wasei="{wasei}">{text}</lsource>')

        source = self.helper.buildAndSaveSource(sense, xml)
        savedEntry = JMdictEntry.objects.get(ent_seq = seq)
        savedSense = JMdictSense.objects.get(id = sense.id)
        savedSource = JMdictSource.objects.get(id = source.id)

        self.assertEqual(savedEntry.ent_seq, seq)
        self.assertEqual(savedSense.entry, savedEntry)
        self.assertEqual(savedSource.sense, savedSense)
        self.assertEqual(savedSource.content, text)
        self.assertEqual(savedSource.language, lang)
        self.assertEqual(savedSource.partial, True)
        self.assertEqual(savedSource.waseieigo, True)

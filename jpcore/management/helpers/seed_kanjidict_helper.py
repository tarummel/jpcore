from xml.etree import ElementTree as etree

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning

PATH = './resources/kanjidic2.xml'

class SeedKanjiDictHelper():

    def getText(self, xml, element):
        text = xml.find(element) if xml.find(element) else ''
        print(f'text: {text}')
        return text
    
    def getList(self, xml, tag):
        result = []
        elements = xml.findall(tag)
        for e in elements:
            result.append(e.text)
        return result
    
    def buildAndSaveKanji(self, xml):
        print(f'kanji xml: {xml}')
        saved = KDKanji.objects.create(
            kanji = xml.find('literal').text
        )
        return saved

    def buildAndSaveCodePoint(self, xml, kanji):
        print(f'cp xml: {xml}')
        return KDCodePoint.objects.create(
            kanji = kanji,
            ucs = self.getText(xml, './/cp_value[@cp_type="ucs"]'),
            jis208 = self.getText(xml, './/cp_value[@cp_type="jis208"]'),
            jis212 = self.getText(xml, './/cp_value[@cp_type="jis212"]'),
            jis213 = self.getText(xml, './/cp_value[@cp_type="jis213"]')
        )

    def buildAndSaveRadical(self, xml, kanji):
        return KDRadical.objects.create(
            kanji = kanji,
            classical = self.getText(xml, './/rad_value[@rad_type="classical"]'),
            nelson = self.getText(xml, './/rad_value[@rad_type="nelson_c"]')
        )

    def buildAndSaveMisc(self, xml, kanji):
        return KDMisc.objects.create(
            kanji = kanji, 
            grade = self.getText(xml, 'grade'),
            jlpt = self.getText(xml, 'jlpt'),
            strokes = self.getText(xml, 'stroke_count'),
            frequency = self.getText(xml, 'freq'),
            radical_name = self.getList(xml, 'rad_names')
        )

    def buildAndSaveVariant(self, xml, kanji):
        return KDVariant.objects.create(
            kanji = kanji, 
            deroo = self.getList(xml, 'ke_pri'),
            jis208 = self.getList(xml, 'ke_pri'),
            jis212 = self.getList(xml, 'ke_pri'),
            jis213 = self.getList(xml, 'ke_pri'),
            nelson = self.getList(xml, 'ke_pri'),
            njecd = self.getList(xml, 'ke_pri'),
            oneill = self.getList(xml, 'ke_pri'),
            sh = self.getList(xml, 'ke_pri')
        )

    def buildAndSaveIndex(self, xml, kanji):
        return KDIndex.objects.create(
            kanji = kanji,
            busy_people = self.getList(xml, 'ke_pri'),
            crowley = self.getList(xml, 'ke_pri'),
            gakken = self.getList(xml, 'ke_pri'),
            halpern_kkd = self.getList(xml, 'ke_pri'),
            halpern_kkld = self.getList(xml, 'ke_pri'),
            halpern_kkld_2nd = self.getList(xml, 'ke_pri'),
            halpern_njecd = self.getList(xml, 'ke_pri'),
            henshall = self.getList(xml, 'ke_pri'),
            henshall3 = self.getList(xml, 'ke_pri'),
            heisig = self.getList(xml, 'ke_pri'),
            heisig6 = self.getList(xml, 'ke_pri'),
            jf_cards = self.getList(xml, 'ke_pri'),
            kanji_in_context = self.getList(xml, 'ke_pri'),
            kodansha_compact = self.getList(xml, 'ke_pri'),
            maniette = self.getList(xml, 'ke_pri'),
            moro = self.getList(xml, 'ke_pri'),
            moro_volume = self.getList(xml, 'ke_pri'),
            moro_page = self.getList(xml, 'ke_pri'),
            nelson_c = self.getList(xml, 'ke_pri'),
            nelson_n = self.getList(xml, 'ke_pri'),
            oneill_names = self.getList(xml, 'ke_pri'),
            oneill_kk = self.getList(xml, 'ke_pri'),
            sakade = self.getList(xml, 'ke_pri'),
            sh_kk = self.getList(xml, 'ke_pri'),
            sh_kk2 = self.getList(xml, 'ke_pri'),
            tutt_cards = self.getList(xml, 'ke_pri')
        )

    def buildAndSaveQueryCode(self, xml, kanji):
        return KDQueryCode.objects.create(
            kanji = kanji,
            skip = self.getList(xml, 'ke_pri'),
            sh_descriptor = self.getList(xml, 'ke_pri'),
            four_corner = self.getList(xml, 'ke_pri'),
            deroo = self.getList(xml, 'ke_pri'),
            misclass_pos = self.getList(xml, 'ke_pri'),
            misclass_strokes = self.getList(xml, 'ke_pri'),
            misclass_strokes_diff = self.getList(xml, 'ke_pri'),
            misclass_strokes_pos = self.getList(xml, 'ke_pri')
        )

    def buildAndSaveReading(self, xml, kanji):
        return KDReading.objects.create(
            kanji = kanji, 
            ch_pinyin = self.getList(xml, 'ke_pri'),
            ko_romanized = self.getList(xml, 'ke_pri'),
            ko_hangul = self.getList(xml, 'ke_pri'),
            vi_chu = self.getList(xml, 'ke_pri'),
            ja_on = self.getList(xml, 'ke_pri'),
            ja_kun = self.getList(xml, 'ke_pri'),
            ja_nanori = self.getList(xml, '')
        )

    def buildAndSaveMeaning(self, xml, kanji):
        return KDMeaning.objects.create(
            kanji = kanji, 
            en = self.getList(xml, 'ke_pri')
        )

    def handle(self):
        
        count = 0
        
        xmlp = etree.XMLParser(encoding="utf-8")
        tree = etree.parse(f'{PATH}', parser = xmlp)
        xmlRoot = tree.getroot()

        for character in xmlRoot.iter('character'):
            print(f'character: {character}')
            count += 1
            key = self.buildAndSaveKanji(character)

            codePoint = character.find('codepoint')
            self.buildAndSaveCodePoint(codePoint, key)

            radical = character.find('radical')
            self.buildAndSaveRadical(radical, key)
            
            misc = character.find('misc')
            self.buildAndSaveMisc(misc, key)

            variant = character.find('misc')
            self.buildAndSaveVariant(variant, key)

            index = character.find('dic_number')
            self.buildAndSaveIndex(index, key)

            queryCode = character.find('query_code')
            self.buildAndSaveIndex(queryCode, key)

            reading = character.find('./reading_meaning')
            self.buildAndSaveReading(reading, key)

            meaning = character.find('./reading_meaning/rmgroup')
            self.buildAndSaveMeaning(meaning, key)

        print(f'Kanji: {count}')
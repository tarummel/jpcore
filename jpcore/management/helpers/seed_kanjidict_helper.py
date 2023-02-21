from lxml import etree

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning

PATH = './resources/kanjidic2.xml'
XML_NAMESPACE = '{http://www.w3.org/XML/1998/namespace}'


class SeedKanjiDictHelper():

    def getText(self, xml, element):
        content = ''
        match = xml.find(element)
        if type(match) == etree._Element:
            content = match.text
        return content
    
    def getList(self, xml, tag):
        result = []
        elements = xml.findall(tag)
        for e in elements:
            result.append(e.text)
        return result
    
    def buildAndSaveKanji(self, xml):
        saved = KDKanji.objects.create(
            kanji = xml.find('literal').text
        )
        return saved

    def buildAndSaveCodePoint(self, xml, kanji):
        return KDCodePoint.objects.create(
            kanji = kanji,
            ucs = self.getText(xml, 'cp_value[@cp_type="ucs"]'),
            jis208 = self.getText(xml, 'cp_value[@cp_type="jis208"]'),
            jis212 = self.getText(xml, 'cp_value[@cp_type="jis212"]'),
            jis213 = self.getText(xml, 'cp_value[@cp_type="jis213"]')
        )

    def buildAndSaveRadical(self, xml, kanji):
        return KDRadical.objects.create(
            kanji = kanji,
            classical = self.getText(xml, 'rad_value[@rad_type="classical"]'),
            nelson = self.getText(xml, 'rad_value[@rad_type="nelson_c"]')
        )

    def buildAndSaveMisc(self, xml, kanji):
        return KDMisc.objects.create(
            kanji = kanji, 
            grade = self.getText(xml, 'grade'),
            jlpt = self.getText(xml, 'jlpt'),
            strokes = self.getText(xml, 'stroke_count'),
            frequency = self.getText(xml, 'freq'),
            radical_names = self.getList(xml, 'rad_name')
        )

    def buildAndSaveVariant(self, xml, kanji):
        return KDVariant.objects.create(
            kanji = kanji, 
            deroo = self.getText(xml, 'variant[@var_type="deroo"]'),
            jis208 = self.getText(xml, 'variant[@var_type="jis208"]'),
            jis212 = self.getText(xml, 'variant[@var_type="jis212"]'),
            jis213 = self.getText(xml, 'variant[@var_type="jis213"]'),
            nelson_c = self.getText(xml, 'variant[@var_type="nelson_c"]'),
            halpern_njecd = self.getText(xml, 'variant[@var_type="njecd"]'),
            oneill = self.getText(xml, 'variant[@var_type="oneill"]'),
            sh = self.getText(xml, 'variant[@var_type="s_h"]')
        )

    def buildAndSaveIndex(self, xml, kanji):
        return KDIndex.objects.create(
            kanji = kanji,
            busy_people = self.getText(xml, 'dic_ref[@dr_type="busy_people"]'),
            crowley = self.getText(xml, 'dic_ref[@dr_type="crowley"]'),
            gakken = self.getText(xml, 'dic_ref[@dr_type="gakken"]'),
            halpern_kkd = self.getText(xml, 'dic_ref[@dr_type="halpern_kkd"]'),
            halpern_kkld = self.getText(xml, 'dic_ref[@dr_type="halpern_kkld"]'),
            halpern_kkld_2nd = self.getText(xml, 'dic_ref[@dr_type="halpern_kkld_2nd"]'),
            halpern_njecd = self.getText(xml, 'dic_ref[@dr_type="halpern_njecd"]'),
            henshall = self.getText(xml, 'dic_ref[@dr_type="henshall"]'),
            henshall3 = self.getText(xml, 'dic_ref[@dr_type="henshall3"]'),
            heisig = self.getText(xml, 'dic_ref[@dr_type="heisig"]'),
            heisig6 = self.getText(xml, 'dic_ref[@dr_type="heisig6"]'),
            jf_cards = self.getText(xml, 'dic_ref[@dr_type="jf_cards"]'),
            kanji_in_context = self.getText(xml, 'dic_ref[@dr_type="kanji_in_context"]'),
            kodansha_compact = self.getText(xml, 'dic_ref[@dr_type="derkodansha_compactoo"]'),
            maniette = self.getText(xml, 'dic_ref[@dr_type="maniette"]'),
            moro = self.getText(xml, 'dic_ref[@dr_type="FILL"]'),
            moro_volume = self.getText(xml, 'dic_ref[@dr_type="FILL"]'),
            moro_page = self.getText(xml, 'dic_ref[@dr_type="FILL"]'),
            nelson_c = self.getText(xml, 'dic_ref[@dr_type="nelson_c"]'),
            nelson_n = self.getText(xml, 'dic_ref[@dr_type="nelson_n"]'),
            oneill_names = self.getText(xml, 'dic_ref[@dr_type="oneill_names"]'),
            oneill_kk = self.getText(xml, 'dic_ref[@dr_type="oneill_kk"]'),
            sakade = self.getText(xml, 'dic_ref[@dr_type="sakade"]'),
            sh_kk = self.getText(xml, 'dic_ref[@dr_type="sh_kk"]'),
            sh_kk2 = self.getText(xml, 'dic_ref[@dr_type="sh_kk2"]'),
            tutt_cards = self.getText(xml, 'dic_ref[@dr_type="tutt_cards"]')
        )

    def buildAndSaveQueryCode(self, xml, kanji):
        return KDQueryCode.objects.create(
            kanji = kanji,
            skip = self.getText(xml, 'q_code[@qc_type="skip"]'),
            sh_descriptor = self.getText(xml, 'q_code[@qc_type="sh_desc"]'),
            four_corner = self.getText(xml, 'q_code[@qc_type="four_corner"]'),
            deroo = self.getText(xml, 'q_code[@qc_type="deroo"]'),
            misclass_pos = self.getText(xml, 'q_code[@qc_type="skip"][@skip_misclass="posn"]'),
            misclass_strokes = self.getText(xml, 'q_code[@qc_type="skip"][@skip_misclass="stroke_count"]'),
            misclass_strokes_diff = self.getText(xml, 'q_code[@qc_type="skip"][@skip_misclass="stroke_diff"]'),
            misclass_strokes_pos = self.getText(xml, 'q_code[@qc_type="skip"][@skip_misclass="stroke_and_posn"]')
        )

    def buildAndSaveReading(self, xml, kanji):
        path = 'rmgroup'
        return KDReading.objects.create(
            kanji = kanji, 
            ch_pinyin = self.getList(xml, f'{path}/reading[@r_type="pinyin"]'),
            ko_romanized = self.getList(xml, f'{path}/reading[@r_type="korean_r"]'),
            ko_hangul = self.getList(xml, f'{path}/reading[@r_type="korean_h"]'),
            vi_chu = self.getList(xml, f'{path}/reading[@r_type="vietnam"]'),
            ja_on = self.getList(xml, f'{path}/reading[@r_type="ja_on"]'),
            ja_kun = self.getList(xml, f'{path}/reading[@r_type="ja_kun"]'),
            ja_nanori = self.getList(xml, 'nanori')
        )

    def buildAndSaveMeaning(self, xml, kanji):
        return KDMeaning.objects.create(
            kanji = kanji, 
            en = self.getList(xml, 'meaning')
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
import json as JSON
from http import HTTPStatus
from django.test import TestCase, Client

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning
from . import TestHelper


class KanjiDicViewsTestCase(TestCase):
    client = Client()
    helper = TestHelper()

    def setUp(self):
        self.kanji = KDKanji.objects.create(
            kanji = '悪'
        )
        self.cpoint = KDCodePoint.objects.create(
            kanji = self.kanji,
            ucs = 'test',
            jis208 = '',
            jis212 = 'test',
            jis213 = ''
        )
        self.radical = KDRadical.objects.create(
            kanji = self.kanji,
            classical = 'test',
            nelson = ''
        )
        self.misc = KDMisc.objects.create(
            kanji = self.kanji,
            grade = '1',
            jlpt = '4',
            strokes = '7',
            frequency = '253',
            radical_names = ['a']
        )
        self.variant = KDVariant.objects.create(
            kanji = self.kanji,
            deroo = 'test',
            jis208 = '',
            jis212 = '',
            jis213 = '',
            nelson_c = 'test',
            halpern_njecd = '',
            oneill = '',
            sh = ''
        )
        self.index = KDIndex.objects.create(
            kanji = self.kanji,
            busy_people = 'busy_people',
            crowley = 'crowley'
        )
        self.qcode = KDQueryCode.objects.create(
            kanji = self.kanji,
            skip = 'test',
            sh_descriptor = 'test',
            four_corner = 'test',
            deroo = 'test',
            misclass_pos = 'test',
            misclass_strokes = 'test',
            misclass_strokes_diff = 'test',
            misclass_strokes_pos = 'test'
        )
        self.reading = KDReading.objects.create(
            kanji = self.kanji,
            ch_pinyin = ['blah'],
            ko_romanized = ['blah'],
            ko_hangul = ['blah'],
            vi_chu = ['blah'],
            ja_on = ['blah'],
            ja_kun = ['blah'],
            ja_nanori = ['blah']
        )
        self.meaning = KDMeaning.objects.create(
            kanji = self.kanji,
            en = ['']
        )

    def test_get_by_id_success(self):
        url = self.helper.getKDKanjiByIdUrl(self.kanji.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(data['kanji'], self.kanji.kanji)

        cp = data['codepoint'][0]
        self.assertEqual(cp['ucs'], self.cpoint.ucs)
        self.assertFalse(cp.get('jis208'))
        self.assertFalse(cp.get('jis212'))
        self.assertFalse(cp.get('jis213'))

        rad = data['radical'][0]
        self.assertEqual(rad['classical'], self.radical.classical)
        self.assertEqual(rad['nelson'], self.radical.nelson)

        misc = data['misc'][0]
        self.assertEqual(misc['grade'], self.misc.grade)
        self.assertEqual(misc['jlpt'], self.misc.jlpt)
        self.assertEqual(misc['strokes'], self.misc.strokes)
        self.assertEqual(misc['frequency'], self.misc.frequency)
        self.assertEqual(misc['radical_names'], self.misc.radical_names)

        self.assertFalse(data.get('variant'))
        # var = data['variant'][0]
        # self.assertFalse(var.get('deroo'))
        # self.assertFalse(var.get('jis208'))
        # self.assertFalse(var.get('jis208'))
        # self.assertFalse(var.get('jis208'))
        # self.assertEqual(var['nelson_c'], self.variant.nelson_c)
        # self.assertFalse(var.get('halpern_njecd'))
        # self.assertFalse(var.get('oneill'))

        self.assertFalse(data.get('index'))
        # ind = data['index'][0]
        # self.assertFalse(ind.get('busy_people'))
        # self.assertFalse(ind.get('crowley'))
        # self.assertFalse(ind.get('gakken'))
        # self.assertFalse(ind.get('halpern_kkd'))
        # self.assertFalse(ind.get('halpern_kkld'))
        # self.assertFalse(ind.get('halpern_kkld_2nd'))
        # self.assertEqual(ind['halpern_njecd'], self.index.halpern_kkd)
        # self.assertFalse(ind.get('henshall'))
        # self.assertFalse(ind.get('henshall3'))
        # self.assertFalse(ind.get('heisig'))
        # self.assertFalse(ind.get('heisig6'))
        # self.assertFalse(ind.get('jf_cards'))
        # self.assertFalse(ind.get('kanji_in_context'))
        # self.assertFalse(ind.get('kodansha_compact'))
        # self.assertFalse(ind.get('maniette'))
        # self.assertFalse(ind.get('moro'))
        # self.assertFalse(ind.get('moro_volume'))
        # self.assertFalse(ind.get('moro_page'))
        # self.assertEqual(ind['nelson_c'], self.index.nelson_c)
        # self.assertFalse(ind.get('nelson_n'))
        # self.assertFalse(ind.get('oneill_names'))
        # self.assertEqual(ind['oneill_kk'], self.index.oneill_kk)
        # self.assertFalse(ind.get('sakade'))
        # self.assertFalse(ind.get('sh_kk'))
        # self.assertFalse(ind.get('sh_kk2'))
        # self.assertFalse(ind.get('tutt_cards'))
        
        self.assertFalse(data.get('querycode'))
        # qc = data['querycode'][0]
        # self.assertEqual(qc['skip'], self.qcode.skip)
        # self.assertEqual(qc['sh_descriptor'], self.qcode.sh_descriptor)
        # self.assertEqual(qc['four_corner'], self.qcode.four_corner)
        # self.assertFalse(qc.get('deroo'))
        # self.assertFalse(qc.get('misclass_pos'))
        # self.assertFalse(qc.get('misclass_strokes'))
        # self.assertFalse(qc.get('misclass_strokes_diff'))
        # self.assertFalse(qc.get('misclass_strokes_pos'))

        reading = data['reading'][0]
        self.assertFalse(reading.get('ko_romanized'))
        self.assertFalse(reading.get('ko_hangul'))
        self.assertFalse(reading.get('vi_chu'))
        self.assertEqual(reading['ja_on'], self.reading.ja_on)
        self.assertEqual(reading['ja_kun'], self.reading.ja_kun)
        self.assertFalse(reading.get('ja_nanori'))

        meaning = data['meaning'][0]
        self.assertEqual(meaning['en'], self.meaning.en)

    def test_get_by_id_not_found(self):
        url = self.helper.getKDKanjiByIdUrl(0)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKDKanjiByIdUrl(123456789)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_by_id_bad_request(self):
        url = self.helper.getKDKanjiByIdUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    
    def test_get_by_kanji_success(self):
        url = self.helper.getKDKanjiByKanjiUrl(self.kanji.kanji)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(data['kanji'], self.kanji.kanji)

        cp = data['codepoint'][0]
        self.assertEqual(cp['ucs'], self.cpoint.ucs)
        self.assertFalse(cp.get('jis208'))
        self.assertFalse(cp.get('jis212'))
        self.assertFalse(cp.get('jis213'))

        rad = data['radical'][0]
        self.assertEqual(rad['classical'], self.radical.classical)
        self.assertEqual(rad['nelson'], self.radical.nelson)

        misc = data['misc'][0]
        self.assertEqual(misc['grade'], self.misc.grade)
        self.assertEqual(misc['jlpt'], self.misc.jlpt)
        self.assertEqual(misc['strokes'], self.misc.strokes)
        self.assertEqual(misc['frequency'], self.misc.frequency)
        self.assertEqual(misc['radical_names'], self.misc.radical_names)

        self.assertFalse(data.get('variant'))
        # var = data['variant'][0]
        # self.assertFalse(var.get('deroo'))
        # self.assertFalse(var.get('jis208'))
        # self.assertFalse(var.get('jis208'))
        # self.assertFalse(var.get('jis208'))
        # self.assertEqual(var['nelson_c'], self.variant.nelson_c)
        # self.assertFalse(var.get('halpern_njecd'))
        # self.assertFalse(var.get('oneill'))

        self.assertFalse(data.get('index'))
        # ind = data['index'][0]
        # self.assertFalse(ind.get('busy_people'))
        # self.assertFalse(ind.get('crowley'))
        # self.assertFalse(ind.get('gakken'))
        # self.assertFalse(ind.get('halpern_kkd'))
        # self.assertFalse(ind.get('halpern_kkld'))
        # self.assertFalse(ind.get('halpern_kkld_2nd'))
        # self.assertEqual(ind['halpern_njecd'], self.index.halpern_kkd)
        # self.assertFalse(ind.get('henshall'))
        # self.assertFalse(ind.get('henshall3'))
        # self.assertFalse(ind.get('heisig'))
        # self.assertFalse(ind.get('heisig6'))
        # self.assertFalse(ind.get('jf_cards'))
        # self.assertFalse(ind.get('kanji_in_context'))
        # self.assertFalse(ind.get('kodansha_compact'))
        # self.assertFalse(ind.get('maniette'))
        # self.assertFalse(ind.get('moro'))
        # self.assertFalse(ind.get('moro_volume'))
        # self.assertFalse(ind.get('moro_page'))
        # self.assertEqual(ind['nelson_c'], self.index.nelson_c)
        # self.assertFalse(ind.get('nelson_n'))
        # self.assertFalse(ind.get('oneill_names'))
        # self.assertEqual(ind['oneill_kk'], self.index.oneill_kk)
        # self.assertFalse(ind.get('sakade'))
        # self.assertFalse(ind.get('sh_kk'))
        # self.assertFalse(ind.get('sh_kk2'))
        # self.assertFalse(ind.get('tutt_cards'))
        
        self.assertFalse(data.get('querycode'))
        # qc = data['querycode'][0]
        # self.assertEqual(qc['skip'], self.qcode.skip)
        # self.assertEqual(qc['sh_descriptor'], self.qcode.sh_descriptor)
        # self.assertEqual(qc['four_corner'], self.qcode.four_corner)
        # self.assertFalse(qc.get('deroo'))
        # self.assertFalse(qc.get('misclass_pos'))
        # self.assertFalse(qc.get('misclass_strokes'))
        # self.assertFalse(qc.get('misclass_strokes_diff'))
        # self.assertFalse(qc.get('misclass_strokes_pos'))

        reading = data['reading'][0]
        self.assertFalse(reading.get('ko_romanized'))
        self.assertFalse(reading.get('ko_hangul'))
        self.assertFalse(reading.get('vi_chu'))
        self.assertEqual(reading['ja_on'], self.reading.ja_on)
        self.assertEqual(reading['ja_kun'], self.reading.ja_kun)
        self.assertFalse(reading.get('ja_nanori'))

        meaning = data['meaning'][0]
        self.assertEqual(meaning['en'], self.meaning.en)

    def test_get_by_kanji_not_found(self):
        url = self.helper.getKDKanjiByKanjiUrl('扱')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_by_kanji_not_found(self):
        url = self.helper.getKDKanjiByKanjiUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_by_kanji_bad_request(self):
        url = self.helper.getKDKanjiByKanjiUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getKDKanjiByKanjiUrl('too long')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    
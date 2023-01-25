import json as JSON
from http import HTTPStatus
from django.test import TestCase, Client

from jpcore.models import JMdictEntry, JMdictGlossary, JMdictKanji, JMdictReading, JMdictSense, JMdictSource
from . import TestHelper

class KanjiViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.helper = TestHelper()

        self.entry = JMdictEntry.objects.create(ent_seq = 1000000)
        self.kanji1 = JMdictKanji.objects.create(
            id = 7,
            entry = self.entry,
            content = '明', 
            information = 'ateji (phonetic) reading', 
            priorities = ['news1'],
        )
        self.kanji2 = JMdictKanji.objects.create(
            id = 8,
            entry = self.entry,
            content = '白', 
            information = 'word containing irregular kanji usage', 
            priorities = ['news2'],
        )
        self.reading1 = JMdictReading.objects.create(
            id = 3,
            entry = self.entry,
            content = '明', 
            no_kanji = True,
            restrictions = '彼',
            information = '&ok;', 
            priorities = ['ichi1'],
        )
        self.reading2 = JMdictReading.objects.create(
            id = 4,
            entry = self.entry,
            content = '白', 
            no_kanji = False,
            restrictions = 'abc',
            information = 'search-only kana form', 
            priorities = ['ichi2'],
        )
        self.sense1 = JMdictSense.objects.create(
            id = 20, 
            entry = self.entry,
            xreferences = ['知識人'],
            antonyms = ['ドライ・1'],
            parts_of_speech = ['adjective (keiyoushi)'],
            fields = ['linguistics'],
            misc = ['archaic'],
            dialects = ['Hokkaido-ben'],
            information = 'some info'
        )
        self.sense2 = JMdictSense.objects.create(
            id = 21, 
            entry = self.entry,
            xreferences = ['人'],
            antonyms = ['ド'],
            parts_of_speech = ['noun or verb acting prenominally'],
            fields = ['biochemistry'],
            misc = ['character'],
            dialects = ['Kansai-ben'],
            information = 'some other info'
        )
        self.gloss1 = JMdictGlossary.objects.create(
            id = 2, 
            sense = self.sense1, 
            gloss = 'NHK Symphony Orchestra',
            language = 'chi',
            type = 'part'
        )
        self.gloss2 = JMdictGlossary.objects.create(
            id = 3, 
            sense = self.sense2, 
            gloss = 'NHK News',
            language = 'eng',
            type = 'expl'
        )
        self.source1 = JMdictSource.objects.create(
            id = 49,
            sense = self.sense1,
            content = 'bēngzi',
            language = 'chi',
            partial = False,
            waseieigo = False,
        )
        self.source2 = JMdictSource.objects.create(
            id = 50,
            sense = self.sense2,
            content = 'Abend',
            language = 'ger',
            partial = True,
            waseieigo = True,
        )

    def test_get_success(self):
        url = self.helper.getKanjiUrl(self.kanji1.content)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertTrue('jkanji' in data)
        self.assertTrue('jreading' in data)
        self.assertTrue('jsense' in data)

        jk, jr, jse = data['jkanji'], data['jreading'], data['jsense']
        self.assertEqual(len(jk), 2)
        self.assertEqual(len(jr), 2)
        self.assertEqual(len(jse), 2)

        jk1, jk2 = jk[0], jk[1]
        self.assertEqual(jk1['content'], self.kanji1.content)
        self.assertEqual(jk1['information'], self.kanji1.information)
        self.assertEqual(jk1['priorities'], self.kanji1.priorities)
        self.assertEqual(jk2['content'], self.kanji2.content)
        self.assertEqual(jk2['information'], self.kanji2.information)
        self.assertEqual(jk2['priorities'], self.kanji2.priorities)

        jr1, jr2 = jr[0], jr[1]
        self.assertEqual(jr1['content'], self.reading1.content)
        # self.assertEqual(jr1['no_kanji'], self.reading1.no_kanji)
        self.assertEqual(jr1['restrictions'], self.reading1.restrictions)
        self.assertEqual(jr1['information'], self.reading1.information)
        self.assertEqual(jr1['priorities'], self.reading1.priorities)
        self.assertEqual(jr2['content'], self.reading2.content)
        # self.assertEqual(jr2['no_kanji'], self.reading2.no_kanji)
        self.assertEqual(jr2['restrictions'], self.reading2.restrictions)
        self.assertEqual(jr2['information'], self.reading2.information)
        self.assertEqual(jr2['priorities'], self.reading2.priorities)

        jse1, jse2 = jse[0], jse[1]
        self.assertTrue('jglossary' in jse1)
        self.assertEqual(len(jse1['jglossary']), 1)
        self.assertTrue('jsource' in jse1)
        self.assertEqual(len(jse1['jsource']), 1)
        self.assertEqual(jse1['xreferences'], self.sense1.xreferences)
        self.assertEqual(jse1['antonyms'], self.sense1.antonyms)
        self.assertEqual(jse1['parts_of_speech'], self.sense1.parts_of_speech)
        self.assertEqual(jse1['fields'], self.sense1.fields)
        self.assertEqual(jse1['misc'], self.sense1.misc)
        self.assertEqual(jse1['dialects'], self.sense1.dialects)
        self.assertEqual(jse1['information'], self.sense1.information)
        self.assertTrue('jglossary' in jse2)
        self.assertEqual(len(jse2['jglossary']), 1)
        self.assertTrue('jsource' in jse2)
        self.assertEqual(len(jse2['jsource']), 1)
        self.assertEqual(jse2['xreferences'], self.sense2.xreferences)
        self.assertEqual(jse2['antonyms'], self.sense2.antonyms)
        self.assertEqual(jse2['parts_of_speech'], self.sense2.parts_of_speech)
        self.assertEqual(jse2['fields'], self.sense2.fields)
        self.assertEqual(jse2['misc'], self.sense2.misc)
        self.assertEqual(jse2['dialects'], self.sense2.dialects)
        self.assertEqual(jse2['information'], self.sense2.information)

        jg1, jg2 = jse1['jglossary'][0], jse2['jglossary'][0]
        self.assertEqual(jg1['gloss'], self.gloss1.gloss)
        self.assertEqual(jg1['language'], self.gloss1.language)
        self.assertEqual(jg1['type'], self.gloss1.type)
        self.assertEqual(jg2['gloss'], self.gloss2.gloss)
        self.assertEqual(jg2['language'], self.gloss2.language)
        self.assertEqual(jg2['type'], self.gloss2.type)

        jso1, jso2 = jse1['jsource'][0], jse2['jsource'][0]
        self.assertEqual(jso1['content'], self.source1.content)
        self.assertEqual(jso1['language'], self.source1.language)
        self.assertEqual(jso1['partial'], self.source1.partial)
        self.assertEqual(jso1['waseieigo'], self.source1.waseieigo)
        self.assertEqual(jso2['content'], self.source2.content)
        self.assertEqual(jso2['language'], self.source2.language)
        self.assertEqual(jso2['partial'], self.source2.partial)
        self.assertEqual(jso2['waseieigo'], self.source2.waseieigo)

    def test_get_not_found(self):
        url = self.helper.getKanjiUrl('')
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiUrl(' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiUrl(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiUrl('人')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_bad_request(self):
        url = self.helper.getKanjiUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getKanjiUrl('too long')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

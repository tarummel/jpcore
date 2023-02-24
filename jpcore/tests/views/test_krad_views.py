import json as JSON
from http import HTTPStatus
from django.test import TestCase, Client

from jpcore.models import Kanji, Radical
from . import TestHelper


class KradViewsTestCase(TestCase):
    
    def setUp(self):
        self.helper = TestHelper()
        self.client = Client()

        self.rad1 = Radical.objects.create(number = 12, radical = '儿', strokes = 2, meaning = 'eight', reading = 'はちがしら', frequency = 1127, notes = '')
        self.rad2 = Radical.objects.create(number = 109, radical = '目', strokes = 5, meaning = 'eye', reading = 'め', frequency = 819, notes = '')
        self.rad3 = Radical.objects.create(number = 147, radical = '見', strokes = 7, meaning = 'to see', reading = 'みる', frequency = 70, notes = '')
        
        self.oneRadKan = Kanji.objects.create(kanji = '目', strokes = 5)
        self.manyRadKan = Kanji.objects.create(kanji = '見', strokes = 7)
        self.oneRadKan.radicals.set([self.rad2])
        self.manyRadKan.radicals.set([self.rad1, self.rad2, self.rad3])

    def test_list_success(self):
        url = self.helper.listRadicalsUrl()
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 3)

        r1, r2, r3 = data[0], data[1], data[2]
        self.assertEqual(r1['number'], self.rad1.number)
        self.assertEqual(r1['radical'], self.rad1.radical)
        self.assertEqual(r1['strokes'], self.rad1.strokes)
        self.assertEqual(r1['meaning'], self.rad1.meaning)
        self.assertEqual(r1['reading'], self.rad1.reading)
        self.assertEqual(r1['frequency'], self.rad1.frequency)
        self.assertEqual(r1['notes'], self.rad1.notes)
        self.assertFalse('id' in r1)
        self.assertFalse('kanji_set' in r1)

        self.assertEqual(r2['number'], self.rad2.number)
        self.assertEqual(r2['radical'], self.rad2.radical)
        self.assertEqual(r2['strokes'], self.rad2.strokes)
        self.assertEqual(r2['meaning'], self.rad2.meaning)
        self.assertEqual(r2['reading'], self.rad2.reading)
        self.assertEqual(r2['frequency'], self.rad2.frequency)
        self.assertEqual(r2['notes'], self.rad2.notes)
        self.assertFalse('id' in r2)
        self.assertFalse('kanji_set' in r2)
        
        self.assertEqual(r3['number'], self.rad3.number)
        self.assertEqual(r3['radical'], self.rad3.radical)
        self.assertEqual(r3['strokes'], self.rad3.strokes)
        self.assertEqual(r3['meaning'], self.rad3.meaning)
        self.assertEqual(r3['reading'], self.rad3.reading)
        self.assertEqual(r3['frequency'], self.rad3.frequency)
        self.assertEqual(r3['notes'], self.rad3.notes)
        self.assertFalse('id' in r3)
        self.assertFalse('kanji_set' in r3)

    def test_list_option_stroke_count(self):
        exRad1 = Radical.objects.create(number = 4, radical = '𠂉', strokes = 2, meaning = 'bend, possessive particle no', reading = 'の, no, ノ', frequency = 381, notes = '')
        exRad2 = Radical.objects.create(number = 5, radical = '九', strokes = 2, meaning = 'second, latter', reading = 'おつ, otsu, 乙', frequency = 63, notes = '')

        url = self.helper.listRadicalsUrl()
        response = self.client.get(url, {'simple': 'true'})
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 3)
        
        c2, c5, c7 = data['2'], data['5'], data['7']
        self.assertEqual(c2, [self.rad1.radical, exRad1.radical, exRad2.radical])
        self.assertEqual(c5, [self.rad2.radical])
        self.assertEqual(c7, [self.rad3.radical])

    def test_get_success(self):
        url = self.helper.getRadicalUrl(self.rad1.radical)
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(data['number'], self.rad1.number)
        self.assertEqual(data['radical'], self.rad1.radical)
        self.assertEqual(data['strokes'], self.rad1.strokes)
        self.assertEqual(data['meaning'], self.rad1.meaning)
        self.assertEqual(data['reading'], self.rad1.reading)
        self.assertEqual(data['frequency'], self.rad1.frequency)
        self.assertEqual(data['notes'], self.rad1.notes)
        self.assertFalse('id' in data)
        self.assertFalse('kanji_set' in data)

    def test_get_not_found(self):
        url = self.helper.getRadicalUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        url = self.helper.getRadicalUrl(' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRadicalUrl('ア')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRadicalUrl(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_bad_request(self):
        url = self.helper.getRadicalUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        
        url = self.helper.getRadicalUrl('too long')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_kanji_success(self):
        url = self.helper.getKanjiFromRadicalsUrl(self.rad2.radical)
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data'][0]
        self.assertEqual(data['kanji'], self.oneRadKan.kanji)
        self.assertEqual(data['strokes'], self.oneRadKan.strokes)

    def test_get_kanji_multiple(self):
        radicals = ','.join([self.rad1.radical, self.rad2.radical, self.rad3.radical])
        url = self.helper.getKanjiFromRadicalsUrl(radicals)
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['kanji'], self.manyRadKan.kanji)
        self.assertEqual(data[0]['strokes'], self.manyRadKan.strokes)

    def test_get_kanji_option_stroke_count(self):
        radicals = ','.join([self.rad1.radical, self.rad2.radical, self.rad3.radical])
        url = self.helper.getKanjiFromRadicalsUrl(radicals)
        response = self.client.get(url, {'simple': 'true'})
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['7'], [self.manyRadKan.kanji])

    def test_get_kanji_not_found(self):
        url = self.helper.getKanjiFromRadicalsUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiFromRadicalsUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiFromRadicalsUrl('几')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getKanjiFromRadicalsUrl(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_kanji_bad_request(self):
        url = self.helper.getKanjiFromRadicalsUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getKanjiFromRadicalsUrl('still too long')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_related_radicals(self):
        radicals = ','.join([self.rad2.radical])
        url = self.helper.getRelatedRadicalsUrl(radicals)
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 2)

        r1, r3 = data[0], data[1]
        self.assertEqual(r1['number'], self.rad1.number)
        self.assertEqual(r1['radical'], self.rad1.radical)
        self.assertEqual(r1['strokes'], self.rad1.strokes)
        self.assertEqual(r1['meaning'], self.rad1.meaning)
        self.assertEqual(r1['reading'], self.rad1.reading)
        self.assertEqual(r1['frequency'], self.rad1.frequency)
        self.assertEqual(r1['notes'], self.rad1.notes)

        self.assertEqual(r3['number'], self.rad3.number)
        self.assertEqual(r3['radical'], self.rad3.radical)
        self.assertEqual(r3['strokes'], self.rad3.strokes)
        self.assertEqual(r3['meaning'], self.rad3.meaning)
        self.assertEqual(r3['reading'], self.rad3.reading)
        self.assertEqual(r3['frequency'], self.rad3.frequency)
        self.assertEqual(r3['notes'], self.rad3.notes)

    def test_get_related_radicals_simple(self):
        radicals = ','.join([self.rad2.radical])
        url = self.helper.getRelatedRadicalsUrl(radicals)
        response = self.client.get(url, {'simple': 'true'})
        
        self.assertEqual(response.status_code, HTTPStatus.OK)

        json = JSON.loads(response.content)
        self.assertEqual(json['status'], 'success')

        data = json['data']
        self.assertEqual(len(data), 2)
        self.assertEqual(data, [self.rad1.radical, self.rad3.radical])

    def test_get_related_not_found(self):
        url = self.helper.getRelatedRadicalsUrl('a')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRelatedRadicalsUrl('序')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRelatedRadicalsUrl(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRelatedRadicalsUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_related_bad_request(self):
        url = self.helper.getRelatedRadicalsUrl(None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getRelatedRadicalsUrl('a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getRelatedRadicalsUrl('wrong')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        url = self.helper.getRelatedRadicalsUrl('wrong,again')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

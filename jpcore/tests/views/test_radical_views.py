import json as JSON
from http import HTTPStatus
from django.test import TestCase, Client
from jpcore.models import Radical

from . import TestHelper

class RadicalViewsTestCase(TestCase):
    
    def setUp(self):
        self.helper = TestHelper()
        self.client = Client()

        self.rad1 = Radical.objects.create(number = 12, radical = '儿', strokes = 2, meaning = 'eight', reading = 'はちがしら', frequency = 1127, notes = '')
        self.rad2 = Radical.objects.create(number = 109, radical = '目', strokes = 5, meaning = 'eye', reading = 'め', frequency = 819, notes = '')
        self.rad3 = Radical.objects.create(number = 147, radical = '見', strokes = 7, meaning = 'to see', reading = 'みる', frequency = 70, notes = '')
        
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

        self.assertEqual(r2['number'], self.rad2.number)
        self.assertEqual(r2['radical'], self.rad2.radical)
        self.assertEqual(r2['strokes'], self.rad2.strokes)
        self.assertEqual(r2['meaning'], self.rad2.meaning)
        self.assertEqual(r2['reading'], self.rad2.reading)
        self.assertEqual(r2['frequency'], self.rad2.frequency)
        self.assertEqual(r2['notes'], self.rad2.notes)
        
        self.assertEqual(r3['number'], self.rad3.number)
        self.assertEqual(r3['radical'], self.rad3.radical)
        self.assertEqual(r3['strokes'], self.rad3.strokes)
        self.assertEqual(r3['meaning'], self.rad3.meaning)
        self.assertEqual(r3['reading'], self.rad3.reading)
        self.assertEqual(r3['frequency'], self.rad3.frequency)
        self.assertEqual(r3['notes'], self.rad3.notes)

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

    def test_get_not_found(self):
        url = self.helper.getRadicalUrl('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        
        url = self.helper.getRadicalUrl(' ')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRadicalUrl('1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRadicalUrl('a')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        url = self.helper.getRadicalUrl('ア')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_bad_request(self):
        url = self.helper.getRadicalUrl('儿儿')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

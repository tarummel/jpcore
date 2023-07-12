from django.test import TestCase, Client
from http import HTTPStatus


class OtherViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_healthcheck(self):
        response = self.client.get('/healthcheck/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

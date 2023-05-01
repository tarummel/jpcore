from decimal import Decimal
from django.test import TestCase
from jpcore.models import KDKanji, VisualCloseness


class VisualClosenessTestCase(TestCase):
    
    def test_create(self):
        decimal = Decimal('0.900')
        self.leftKanji = KDKanji.objects.create(
            kanji = '左'
        )
        self.rightKanji = KDKanji.objects.create(
            kanji = '右'
        )
        self.vcloseness = VisualCloseness.objects.create(
            left = self.leftKanji,
            right = self.rightKanji,
            sed = decimal
        )

        savedVC = VisualCloseness.objects.get(left = self.leftKanji)

        self.assertEqual(savedVC.left, self.leftKanji)
        self.assertEqual(savedVC.right, self.rightKanji)
        self.assertEqual(savedVC.sed, decimal)

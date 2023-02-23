from django.test import TestCase
from jpcore.models import KDKanji, KDQueryCode


class KDQueryCodeTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        qc = KDQueryCode.objects.create(
            kanji = kanji,
            skip = '1-1-1',
            sh_descriptor = '4i10.1',
            four_corner = '2024.7',
            deroo = '2067',
            misclass_pos = '12',
            misclass_strokes = '4-1-1',
            misclass_strokes_diff = '1-2-3',
            misclass_strokes_pos = '2-1-4'
        )
        saved = KDQueryCode.objects.get(id = qc.id)
        
        self.assertEqual(saved.skip, qc.skip)
        self.assertEqual(saved.sh_descriptor, qc.sh_descriptor)
        self.assertEqual(saved.four_corner, qc.four_corner)
        self.assertEqual(saved.deroo, qc.deroo)
        self.assertEqual(saved.misclass_pos, qc.misclass_pos)
        self.assertEqual(saved.misclass_strokes, qc.misclass_strokes)
        self.assertEqual(saved.misclass_strokes_diff, qc.misclass_strokes_diff)
        self.assertEqual(saved.misclass_strokes_pos, qc.misclass_strokes_pos)
    
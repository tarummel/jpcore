from django.test import TestCase
from jpcore.models import KDKanji, KDVariant


class KDVariantTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        misc = KDVariant.objects.create(
            kanji = kanji,
            jis208 = '1',
            jis212 = '25',
            jis213 = '7',
            nelson_c = '4',
            halpern_njecd = '4',
            oneill = '4',
            sh = '4'
        )
        saved = KDVariant.objects.get(id = misc.id)
        
        self.assertEqual(saved.jis208, misc.jis208)
        self.assertEqual(saved.jis212, misc.jis212)
        self.assertEqual(saved.jis213, misc.jis213)
        self.assertEqual(saved.nelson_c, misc.nelson_c)
        self.assertEqual(saved.halpern_njecd, misc.halpern_njecd)
        self.assertEqual(saved.oneill, misc.oneill)
        self.assertEqual(saved.sh, misc.sh)

from django.test import TestCase
from jpcore.models import KDKanji, KDIndex


class KDIndexTestCase(TestCase):

    def test_create(self):
        kanji = KDKanji.objects.create(kanji = '尶')
        index = KDIndex.objects.create(
            kanji = kanji,
            busy_people = '1',
            crowley = '1',
            gakken = '1',
            halpern_kkd = '1',
            halpern_kkld = '1',
            halpern_kkld_2nd = '1',
            halpern_njecd = '1',
            henshall = '1',
            henshall3 = '1',
            heisig = '1',
            heisig6 = '1',
            jf_cards = '1',
            kanji_in_context = '1',
            kodansha_compact = '1',
            maniette = '1',
            moro = '1',
            moro_volume = '1',
            moro_page = '1',
            nelson_c = '1',
            nelson_n = '1',
            oneill_names = '1',
            oneill_kk = '1',
            sakade = '1',
            sh_kk = '1',
            sh_kk2 = '1',
            tutt_cards = '1'

        )
        saved = KDIndex.objects.get(id = index.id)
        
        self.assertEqual(saved.busy_people, index.busy_people)
        self.assertEqual(saved.crowley, index.crowley)
        self.assertEqual(saved.gakken, index.gakken)
        self.assertEqual(saved.halpern_kkd, index.halpern_kkd)
        self.assertEqual(saved.halpern_kkld, index.halpern_kkld)
        self.assertEqual(saved.halpern_kkld_2nd, index.halpern_kkld_2nd)
        self.assertEqual(saved.halpern_njecd, index.halpern_njecd)
        self.assertEqual(saved.henshall, index.henshall)
        self.assertEqual(saved.henshall3, index.henshall3)
        self.assertEqual(saved.heisig, index.heisig)
        self.assertEqual(saved.heisig6, index.heisig6)
        self.assertEqual(saved.jf_cards, index.jf_cards)
        self.assertEqual(saved.kanji_in_context, index.kanji_in_context)
        self.assertEqual(saved.kodansha_compact, index.kodansha_compact)
        self.assertEqual(saved.maniette, index.maniette)
        self.assertEqual(saved.moro, index.moro)
        self.assertEqual(saved.moro_volume, index.moro_volume)
        self.assertEqual(saved.moro_page, index.moro_page)
        self.assertEqual(saved.nelson_c, index.nelson_c)
        self.assertEqual(saved.nelson_n, index.nelson_n)
        self.assertEqual(saved.oneill_names, index.oneill_names)
        self.assertEqual(saved.oneill_kk, index.oneill_kk)
        self.assertEqual(saved.sakade, index.sakade)
        self.assertEqual(saved.sh_kk, index.sh_kk)
        self.assertEqual(saved.sh_kk2, index.sh_kk2)
        self.assertEqual(saved.tutt_cards, index.tutt_cards)

from django.db import models


# This element contains the index numbers and similar unstructured information such as page numbers in a number of 
# published dictionaries, and instructional books on kanji.
class KDIndex(models.Model):

    kanji = models.ForeignKey('KDKanji', on_delete = models.CASCADE, related_name = 'kdindex')
    
    busy_people = models.TextField(blank = True)
    crowley = models.TextField(blank = True)
    gakken = models.TextField(blank = True)
    halpern_kkd = models.TextField(blank = True)
    halpern_kkld = models.TextField(blank = True)
    halpern_kkld_2nd = models.TextField(blank = True)
    halpern_njecd = models.TextField(blank = True)
    henshall = models.TextField(blank = True)
    henshall3 = models.TextField(blank = True)
    heisig = models.TextField(blank = True)
    heisig6 = models.TextField(blank = True)
    jf_cards = models.TextField(blank = True)
    kanji_in_context = models.TextField(blank = True)
    kodansha_compact = models.TextField(blank = True)
    maniette = models.TextField(blank = True)
    moro = models.TextField(blank = True)
    moro_volume = models.TextField(blank = True)
    moro_page = models.TextField(blank = True)
    nelson_c = models.TextField(blank = True)
    nelson_n = models.TextField(blank = True)
    oneill_names = models.TextField(blank = True)
    oneill_kk = models.TextField(blank = True)
    sakade = models.TextField(blank = True)
    sh_kk = models.TextField(blank = True)
    sh_kk2 = models.TextField(blank = True)
    tutt_cards = models.TextField(blank = True)

    def __str__(self):
        return f'nelson_c: {self.nelson_c}'

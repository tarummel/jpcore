from jpcore.models import KDQueryCode


API_PREFIX = '/api'
JM = 'jmdict'
KD = 'kanjidic'
KR = 'krad'

class TestHelper():
    
    def getEntryByIdUrl(self, id: int):
        return f'{API_PREFIX}/{JM}/kanji/{id}/'
    
    def getEntryByCharacterUrl(self, kanji: str):
        return f'{API_PREFIX}/{JM}/kanji/{kanji}/'
    
    def getKDKanjiByIdUrl(self, id: int):
        return f'{API_PREFIX}/{KD}/kanji/{id}/'

    def getKDKanjiByKanjiUrl(self, kanji: str):
        return f'{API_PREFIX}/{KD}/kanji/{kanji}/'

    def getKanjiFromRadicalsUrl(self, radicals):
        return f'{API_PREFIX}/{KD}/radicals/{radicals}/kanji/'

    def listRadicalsUrl(self):
        return f'{API_PREFIX}/{KR}/radicals/'

    def getRadicalUrl(self, radical):
        return f'{API_PREFIX}/{KR}/radicals/{radical}/'

    def getRelatedRadicalsUrl(self, radicals):
        return f'{API_PREFIX}/{KR}/radicals/{radicals}/related/'

    def getKDKanjiRandomUrl(self):
        return f'{API_PREFIX}/{KD}/random/'

    def getKDKanjiBySkipCodeUrl(self, code):
        return f'{API_PREFIX}/{KD}/kanji/skipcode/{code}/'

    def buildKDQueryCode(self, kanji, skip = '1-1-1', ms_pos = []):
        return KDQueryCode.objects.create(
            kanji = kanji,
            skip = skip,
            sh_descriptor = 'test',
            four_corner = 'test',
            deroo = 'test',
            misclass_pos = ms_pos,
            misclass_strokes = [],
            misclass_strokes_diff = [],
            misclass_strokes_pos = []
        )

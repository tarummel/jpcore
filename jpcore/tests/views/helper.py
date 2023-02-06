API_PREFIX = '/api'
RADICALS_PATH = 'radicals'
KANJI_PATH = 'kanji'

class TestHelper():
    def listRadicalsUrl(self):
        return f'{API_PREFIX}/{RADICALS_PATH}/'

    def getRadicalUrl(self, radical):
        return f'{API_PREFIX}/{RADICALS_PATH}/{radical}/'
    
    def getKanjiFromRadicalsUrl(self, radicals):
        return f'{API_PREFIX}/{RADICALS_PATH}/{radicals}/kanji/'

    def getKanjiUrl(self, kanji):
        return f'{API_PREFIX}/{KANJI_PATH}/{kanji}/'
    
    def getKanjiRadicalsUrl(self, kanji):
        return f'{API_PREFIX}/{KANJI_PATH}/{kanji}/radicals/'
    
    def getRelatedRadicalsUrl(self, radicals):
        return f'{API_PREFIX}/{RADICALS_PATH}/{radicals}/related/'
    
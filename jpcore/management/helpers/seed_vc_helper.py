from jpcore.models import KDKanji, VisualCloseness

SED_FILE_PATH = './resources/strokeEditDistance.csv'
YNL_FILE_PATH = './resources/yehAndLiRadical.csv'

# no duplicates stats
# Total: 12257
# Execution time (seconds): unknown wasn't tested with caching

# Current basic implementation which allows for left/right and right/left combinations exist
# If you prevent duplicates by checking for both combinations then certain kanji will be the left or right exclusively
# which results in ambiguity so you have to check both which I believe would be slightly slower vs kilobytes
# Total: 19450
# Execution time (seconds):14.859374284744263

# NOTE: Visual Closeness has a Kanjidic dependency
class SeedVisualClosenessHelper():
    kanjiCache = {}

    def parseLine(self, line):
        return line[0], line[2::].split(" ")

    def getKDKanji(self, kanjiChar):
        if kanjiChar in self.kanjiCache:
            return self.kanjiCache[kanjiChar]
        try:
            saved = KDKanji.objects.get(kanji = kanjiChar)
            self.kanjiCache[saved.kanji] = saved
            return saved
        except Exception as e:
            print('kanji expected and not found did you load kanjidic first?')
            quit()

    def buildAndSaveVisualCloseness(self, left, right, sed):
        return VisualCloseness.objects.create(
            left = left,
            right = right, 
            sed = sed,
            # ynl = 0.000,
        )

    def handle(self):
        count = 0

        with open(SED_FILE_PATH, encoding = "utf-8") as sedFile:
            for line in sedFile:
                # each line has a leftmost base kanji followed by 10 related kanji + closeness value
                left, related = self.parseLine(line)
                for i in range(0, 10):
                    # related kanji is n, the corresponding closeness rating is n + 1
                    right, sed = related[2 * i], related[(2 * i) + 1]
                    self.buildAndSaveVisualCloseness(self.getKDKanji(left), self.getKDKanji(right), sed)
                    count += 1

        # not interested in using since SED seems more useful
        # with open(YNL_FILE_PATH, encoding = "utf-8") as ynlFile:

        print(f'Total: {count}')

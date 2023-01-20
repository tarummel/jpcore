import sys
import time
from django.core.management.base import BaseCommand

from jpcore import models

# Execution time (seconds):25.42658019065857
# Count:54323

RADINFO_PATH = './resources/radinfo.tsv'
KRAD_PATH = './resources/kradfile.txt'

radDict = {}
stats = [0, 0, 0, 0]

class Command(BaseCommand):
    help = 'Seed Krad Command'

    def __init__(self):
        models.Radical.objects.all().delete()
        models.Kanji.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()

        self.loadRadinfo()
        self.kradPrecheck()
        self.loadKrad()

        stats[0] = (time.time() - startTime)

        self.printStats()

    def loadRadinfo(self):
        # format [No \t Radical \t Strokes \t Meaning \t Reading \t Position \t Frequency \t Notes]
        with open(f'{RADINFO_PATH}') as f:
            # skip headers
            next(f)

            for line in f:
                e = line.split('\t')
                if e[1] != '':
                    savedRadical = models.Radical(
                        number = int(e[0]), 
                        radical = e[1],
                        strokes = int(e[2]),
                        meaning = e[3],
                        reading = e[4],
                        position = e[5],
                        frequency = int(e[6]),
                        notes = e[7]
                    )
                    savedRadical.save()
                    stats[1] += 1

                    # lookup for calculating kanji stroke counts later
                    radDict[savedRadical.radical] = savedRadical

    def kradSplit(self, line):
        # format [k : r1 r2 r3]
        split = line.strip().split(' ')
        return split[0], split[2:]

    def kradPrecheck(self):
        allRad = models.Radical.objects.all().values('radical', 'strokes')

        if len(allRad) != stats[0]:
            sys.exit('Mismatched radical count between db and radinfo')

        missing = set()
        with open(f'{KRAD_PATH}') as f:
            for line in f:
                k, radicals = self.kradSplit(line)
                for r in radicals:
                    if r not in radDict:
                        missing.add(r)
        if missing:
            sys.exit(f'unlisted radical(s) found in krad {missing}')

    def loadKrad(self):
        with open(f'{KRAD_PATH}') as f:
            # format [k : r1 r2 r3]
            for line in f:
                kanji, radicals = self.kradSplit(line)
                
                # first pass for stroke count
                strokes = 0
                for r in radicals:
                    strokes += radDict[r].strokes
                    
                # early save as pre-req for ManyToMany relationship
                savedKanji = models.Kanji(kanji = kanji, strokes = strokes)
                savedKanji.save()

                # second pass for adding radicals to Kanji
                for r in radicals:
                    savedKanji.radicals.add(radDict[r])
                    stats[3] += 1
                stats[2] += 1

    def printStats(self):
        print(f'Execution time (seconds):{str(stats[0])}')
        print(f'Kanji: {str(stats[2])}, radicals: {str(stats[1])}, rad/kanji keys: {str(stats[3])}')

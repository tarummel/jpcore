import sys
import time
from django.core.management.base import BaseCommand

from app import models

# Execution time (seconds):25.42658019065857
# Count:54323

RADINFO_PATH = './resources/radinfo.tsv'
KRAD_PATH = './resources/kradfile.txt'

radStrokes = {}
stats = [0, 0]

class Command(BaseCommand):
    help = 'Seed Krad Command'

    def __init__(self):
        models.Radical.objects.all().delete()
        models.Kanji.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()

        self.loadRadicalInfo()
        self.verifyKrad()
        # self.loadKrad()
        # self.postUpdate()

        execTime = (time.time() - startTime)

    def loadRadicalInfo(self):
        # format [No \t Radical \t Strokes \t Meaning \t Reading \t Position \t Frequency \t Notes]
        with open(f'{RADINFO_PATH}') as f:
            # skip headers
            next(f)

            for line in f:
                e = line.split('\t')
                if e[0] != '':
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
                    stats[0] += 1

                    # easy lookup for calculating kanji stroke counts later
                    radStrokes[savedRadical.radical] = savedRadical.strokes
                    

        print(f'Radicals: {stats[0]}')

    def kradSplit(self, line):
        # format [k : r1 r2 r3]
        split = line.strip().split(' ')
        return split[0], split[2:]

    def verifyKrad(self):
        allRad = models.Radical.objects.all().values('radical', 'strokes')

        if len(allRad) != stats[0]:
            sys.exit('Mismatched radical count between db and radinfo')

        with open(f'{KRAD_PATH}') as f:
            for line in f:
                kanji, radicals = self.kradSplit(line)
                for r in radicals:
                    if r not in radStrokes:
                        sys.exit(f'unlisted radical found in krad {r}')


    def loadKrad(self):
        radDict = {}

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
                    savedKanji.add(radDict[r])

                stats[1] += 1

    # def printStats(self):
    #     print(f'Execution time (seconds):{str(execTime)}')
    #     print(f'Kanji: {str(kanjiCount)}, radicals: {str(radicalCount)}')
    #     pass
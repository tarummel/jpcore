import time
from django.core.management.base import BaseCommand

from app import models

# Execution time (seconds):25.42658019065857
# Count:54323

PATH = './resources/kradfile.txt'

class Command(BaseCommand):
    help = 'Seed Krad Command'

    def __init__(self):
        models.KanjiRadical.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()
        kradCount = 0

        with open(f'{PATH}') as f:
            # format [k : r1 r2 r3]
            for line in f:
                split = line.strip().split(' ')
                kanji = split[0]

                for radical in split[2:]:
                    krad = models.KanjiRadical(kanji = kanji, radical = radical)
                    krad.save()
                    kradCount += 1

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')
        print(f'Count:{str(kradCount)}')
import time
from django.core.management.base import BaseCommand

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning
from jpcore.management.helpers import SeedKanjiDictHelper as helper

# Entry:198729, Kanji:204164, Read:238386, Sense:228960, Gloss:395043, Sour:5581
# Execution time (seconds):906.6395170688629

class Command(BaseCommand):
    help = 'Seed KanjiDict Command'

    def __init__(self):
        KDKanji.objects.all().delete()
        KDCodePoint.objects.all().delete()
        KDRadical.objects.all().delete()
        KDMisc.objects.all().delete()
        KDVariant.objects.all().delete()
        KDIndex.objects.all().delete()
        KDQueryCode.objects.all().delete()
        KDReading.objects.all().delete()
        KDMeaning.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()
        
        helper().handle()

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')

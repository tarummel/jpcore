import time
from django.core.management.base import BaseCommand

from jpcore.models import JMdictEntry, JMdictKanji, JMdictReading, JMdictSense, JMdictGlossary, JMdictSource
from jpcore.management.helpers import SeedJMdictHelper as helper

# Entry:198729, Kanji:204164, Read:238386, Sense:228960, Gloss:395043, Sour:5581
# Execution time (seconds):906.6395170688629

class Command(BaseCommand):
    help = 'Seed JMdict Command'

    def __init__(self):
        JMdictEntry.objects.all().delete()
        JMdictKanji.objects.all().delete()
        JMdictReading.objects.all().delete()
        JMdictSense.objects.all().delete()
        JMdictGlossary.objects.all().delete()
        JMdictSource.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()
        
        helper().handle()

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')

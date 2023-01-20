import time
from django.core.management.base import BaseCommand

from jpcore import models
from jpcore.management.helpers import SeedJMdictHelper as helper

# Entry:198729, Kanji:204164, Read:238386, Sense:228960, Gloss:395043, Sour:5581
# Execution time (seconds):906.6395170688629

class Command(BaseCommand):
    help = 'Seed JMdict Command'

    def __init__(self):
        models.JMdictEntry.objects.all().delete()
        models.JMdictKanji.objects.all().delete()
        models.JMdictReading.objects.all().delete()
        models.JMdictSense.objects.all().delete()
        models.JMdictGlossary.objects.all().delete()
        models.JMdictSource.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()
        
        helper().handle()

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')

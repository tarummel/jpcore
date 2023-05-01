import time
from django.core.management.base import BaseCommand

from jpcore.models import VisualCloseness
from jpcore.management.helpers import SeedVisualClosenessHelper as helper

# Total: 19450
# Execution time (seconds):14.859374284744263

# NOTE: Visual Closeness has a Kanjidic dependency
class Command(BaseCommand):
    help = 'Seed Visual Closeness Command'

    def __init__(self):
        VisualCloseness.objects.all().delete()

    def handle(self, *args, **options):
        startTime = time.time()
        
        helper().handle()

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')

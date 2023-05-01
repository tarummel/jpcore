import time
from django.core.management.base import BaseCommand

from jpcore.models import KDKanji, KDCodePoint, KDRadical, KDMisc,  KDVariant, KDIndex, KDQueryCode, KDReading, KDMeaning, SkipCode
from django.core import management

class Command(BaseCommand):
    help = 'Seed All Command'

    def handle(self, *args, **options):
        management.call_command("seed_krad")
        management.call_command("seed_jmdict")
        management.call_command("seed_kanjidic")

        # Kanjidic Dependency
        # management.call_command("seed_vc")

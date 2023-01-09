#!/usr/bin/env python

import os
import time
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from app import models

PATH = './resources/JMdict_e.xml'

class Command(BaseCommand):
    help = 'Seed JMdict Command'

    def __init__(self):
        models.JMdictEntry.objects.all().delete()
        models.JMdictKanji.objects.all().delete()
        models.JMdictReading.objects.all().delete()
        models.JMdictSense.objects.all().delete()
        models.JMdictGlossary.objects.all().delete()

    def getTextIfExists(self, content, tag):
        element = content.find(tag)
        xmlstr = ET.tostring(element, encoding='unicode', method='xml')
        print(xmlstr)
        # if xmlstr:
        #     return xmlstr.text
        return ''

    def getListIfExists(self, content, tag):
        result = []
        elements = content.findall(tag)
        for e in elements:
            result.append(e.text)
        return result

    def handle(self, *args, **options):
        tree = ET.parse(f'{PATH}')
        xmlRoot = tree.getroot()

        startTime = time.time()

        for jmEntry in xmlRoot.iter('entry'):
            ent_seq = int(jmEntry.find('ent_seq').text)
            entry = models.JMdictEntry(ent_seq = ent_seq)
            entry.save()

            for jmKanji in jmEntry.iter('k_ele'):
                keb = self.getTextIfExists(jmKanji, 'keb')
                if keb:
                    print(keb)
                ke_inf = self.getTextIfExists(jmKanji, 'ke_inf')
                ke_pri = self.getListIfExists(jmKanji, 'ke_pri')

                kanji = models.JMdictKanji(entry = entry, element = keb, information = ke_inf, priorities = ke_pri)
                kanji.save()

            for jmReading in jmEntry.iter('r_ele'):
                reb = self.getTextIfExists(jmReading, 'reb')
                re_nokanji = True if jmReading.find('re_nokanji') else False
                re_restr = self.getTextIfExists(jmReading, 're_restr')
                re_inf = self.getTextIfExists(jmReading, 're_inf')
                re_pri = self.getListIfExists(jmReading, 're_pri')

                reading = models.JMdictReading(
                    entry = entry, 
                    element = reb, 
                    no_kanji = re_nokanji,
                    restrictions = re_restr,
                    information = re_inf,
                    priorities = re_pri
                )
                reading.save()

            for jmSense in jmEntry.iter('sense'):
                sense = models.JMdictSense(entry = entry)
                sense.save()

                for jmGloss in self.getListIfExists(jmSense, 'gloss'):
                    glossary = models.JMdictGlossary(sense = sense, gloss = jmGloss)
                    glossary.save()

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds): {str(execTime)}')

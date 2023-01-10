#!/usr/bin/env python

import time
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from app import models

# Execution time (seconds):860.4005470275879
# Entry:198729, Kanji:204164, Read:238386, Sense:228960, Gloss:395043

PATH = './resources/JMdict_e.xml'

TOTAL_ENTRIES = 198729
TOTAL_KANJI = 204164
TOTAL_READING = 238386
TOTAL_SENSE = 228960
TOTAL_GLOSSES = 395043

class Command(BaseCommand):
    help = 'Seed JMdict Command'

    def __init__(self):
        models.JMdictEntry.objects.all().delete()
        models.JMdictKanji.objects.all().delete()
        models.JMdictReading.objects.all().delete()
        models.JMdictSense.objects.all().delete()
        models.JMdictGlossary.objects.all().delete()
        # models.JMdictSource.objects.all().delete()
        # models.JMdictExample.objects.all().delete()

    # for special char encoding like keb and reb
    def getKanjiTextFromXml(self, content, tag):
        element = ''
        contentStr = ET.tostring(content, encoding = 'unicode', method = 'xml')
        try:
            i = contentStr.index(f'<{tag}>') + len(tag) + 2
            j = contentStr.index(f'</{tag}>', i + 1)
            element = contentStr[i:j]
        except ValueError:
            # print('ValueError: substring not found')
            pass

        return element

    def getTextFromXml(self, content, tag):
        element = content.find(tag)
        if element:
            return element.text
        return ''

    def getListFromXml(self, content, tag):
        result = []
        elements = content.findall(tag)
        for e in elements:
            result.append(e.text)
        return result

    def buildAndSaveEntry(self, content):
        entry = models.JMdictEntry(ent_seq = int(content.find('ent_seq').text))
        entry.save()
        return entry

    def buildAndSaveKanji(self, entry, content):
        kanji = models.JMdictKanji(
            entry = entry, 
            element = self.getKanjiTextFromXml(content, 'keb'), 
            information = self.getKanjiTextFromXml(content, 'ke_inf'), 
            priorities = self.getListFromXml(content, 'ke_pri')
        )
        kanji.save()
        
    def buildAndSaveReading(self, entry, content):
        reading = models.JMdictReading(
            entry = entry, 
            element = self.getKanjiTextFromXml(content, 'reb'), 
            no_kanji = True if content.find('re_nokanji') else False,
            restrictions = self.getKanjiTextFromXml(content, 're_restr'),
            information = self.getKanjiTextFromXml(content, 're_inf'),
            priorities = self.getListFromXml(content, 're_pri')
        )
        reading.save()

    def buildAndSaveSense(self, entry, content):
        sense = models.JMdictSense(entry = entry)
        sense.save()
        return sense

    def buildAndSaveGlossary(self, sense, gloss):
        glossary = models.JMdictGlossary(sense = sense, gloss = gloss)
        glossary.save()

    def handle(self, *args, **options):
        startTime = time.time()
        stats = [0, 0, 0, 0, 0]
        printPercentages = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 100]
        
        tree = ET.parse(f'{PATH}')
        xmlRoot = tree.getroot()

        for jmEntry in xmlRoot.iter('entry'):
            entryKey = self.buildAndSaveEntry(jmEntry)
            stats[0] += 1

            for jmKanji in jmEntry.iter('k_ele'):
                self.buildAndSaveKanji(entryKey, jmKanji)
                stats[1] += 1

            for jmReading in jmEntry.iter('r_ele'):
                self.buildAndSaveReading(entryKey, jmReading)
                stats[2] += 1

            for jmSense in jmEntry.iter('sense'):
                senseKey = self.buildAndSaveSense(entryKey, jmSense)
                stats[3] += 1

                for jmGloss in self.getListFromXml(jmSense, 'gloss'):
                    self.buildAndSaveGlossary(senseKey, jmGloss)
                    stats[4] += 1

            percentComplete = 100 * float(stats[4]) / 395043
            if percentComplete in printPercentages:
                print(f'{str(percentComplete)}%')
            


        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')
        print(f'Entry:{stats[0]}, Kanji:{stats[1]}, Read:{stats[2]}, Sense:{stats[3]}, Gloss:{stats[4]}')

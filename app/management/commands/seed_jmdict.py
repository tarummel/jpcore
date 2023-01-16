#!/usr/bin/env python

import time
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand

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
        models.JMdictSource.objects.all().delete()

    def getAttributes(self, xml, tag):
        pass

    # for special char encoding like keb and reb
    def getKanjiTextFromXml(self, xml, tag):
        element = ''
        xmlStr = ET.tostring(xml, encoding = 'unicode', method = 'xml')
        try:
            i = xmlStr.index(f'<{tag}>') + len(tag) + 2
            j = xmlStr.index(f'</{tag}>', i + 1)
            element = xmlStr[i:j]
        except ValueError:
            # print('ValueError: substring not found')
            pass

        return element

    def getTextFromXml(self, xml, tag):
        element = xml.find(tag)
        if element:
            return element.text
        return ''

    def getListFromXml(self, xml, tag):
        result = []
        elements = xml.findall(tag)
        for e in elements:
            result.append(e.text)
        return result

    def buildAndSaveEntry(self, xml):
        entry = models.JMdictEntry(ent_seq = int(xml.find('ent_seq').text))
        entry.save()
        return entry

    def buildAndSaveKanji(self, entry, xml):
        kanji = models.JMdictKanji(
            entry = entry, 
            content = self.getKanjiTextFromXml(xml, 'keb'), 
            information = self.getKanjiTextFromXml(xml, 'ke_inf'), 
            priorities = self.getListFromXml(xml, 'ke_pri')
        )
        kanji.save()
        
    def buildAndSaveReading(self, entry, xml):
        reading = models.JMdictReading(
            entry = entry, 
            content = self.getKanjiTextFromXml(xml, 'reb'), 
            no_kanji = True if xml.find('re_nokanji') else False,
            restrictions = self.getKanjiTextFromXml(xml, 're_restr'),
            information = self.getKanjiTextFromXml(xml, 're_inf'),
            priorities = self.getListFromXml(xml, 're_pri')
        )
        reading.save()

    def buildAndSaveSense(self, entry, xml):
        sense = models.JMdictSense(
            entry = entry,
            xreferences = self.getListFromXml(xml, 'xref'),
            antonyms = self.getListFromXml(xml, 'ant'),
            parts_of_speech = self.getListFromXml(xml, 'pos'),
            fields = self.getListFromXml(xml, 'field'),
            misc = self.getListFromXml(xml, 'misc'), 
            dialects = self.getListFromXml(xml, 'dial'),
            information = self.getKanjiTextFromXml(xml, 's_inf')
        )
        sense.save()
        return sense

    def buildAndSaveGlossary(self, sense, gloss):
        # TODO: getAttributes function
        glossary = models.JMdictGlossary(
            sense = sense, 
            gloss = gloss,
            # language = ,
            # type = 
        )
        glossary.save()

    def buildAndSaveSource(self, sense, content):
        sense = models.JMdictSource(
            sense = sense,
            content = content,
            # language = ,
            # partial = ,
            # waseieigo = 
        )

    def handle(self, *args, **options):
        stats = [0, 0, 0, 0, 0, 0]
        printPercentages = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 100]
        startTime = time.time()
        
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

                for jmSource in self.getListFromXml(jmSense, 'lsource'):
                    self.buildAndSaveSource(senseKey, jmSource)
                    stats[5] += 1


            percentComplete = round(100 * float(stats[4]) / 395043)
            if percentComplete in printPercentages:
                printPercentages.remove(percentComplete)
                print(f'{str(percentComplete)}%')

        execTime = (time.time() - startTime)
        print(f'Execution time (seconds):{str(execTime)}')
        print(f'Entry:{stats[0]}, Kanji:{stats[1]}, Read:{stats[2]}, Sense:{stats[3]}, Gloss:{stats[4]}, Sour:{stats[5]}')

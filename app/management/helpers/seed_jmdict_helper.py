from xml.etree import ElementTree as etree

from app import models

PATH = './resources/JMdict_e.xml'
XML_NAMESPACE = '{http://www.w3.org/XML/1998/namespace}'
TOTAL_ENTRIES = 198729
TOTAL_KANJIS = 204164
TOTAL_READINGS = 238386
TOTAL_SENSES = 228960
TOTAL_GLOSSES = 395043
TOTAL_SOURCES = 5581

stats = [0, 0, 0, 0, 0, 0]

class SeedJMdictHelper():
    # for gloss and lsource only
    def getTextWithAttributes(self, xml):
        element = ''
        if xml and xml.text:
            element = xml.text

        attributes = {}
        for a in xml.attrib:
            attrName = a if a[0] != '{' else a.replace(XML_NAMESPACE, '')
            attrValue = xml.attrib[a]
            attributes[attrName] = attrValue

        return element, attributes

    # TODO: find a better way
    def getText(self, xml, tag):
        element = ''
        xmlStr = etree.tostring(xml, encoding = 'unicode', method = 'xml')
        try:
            i = xmlStr.index(f'<{tag}>') + len(tag) + 2
            j = xmlStr.index(f'</{tag}>', i + 1)
            element = xmlStr[i:j]
        except ValueError:
            # print('ValueError: substring not found')
            pass

        return element

    def getList(self, xml, tag):
        result = []
        elements = xml.findall(tag)
        for e in elements:
            result.append(e.text)
        return result

    def buildAndSaveEntry(self, xml):
        entry = models.JMdictEntry(ent_seq = int(xml.find('ent_seq').text))
        entry.save()
        return entry

    def buildAndSaveKanji(self, entryObj, xml):
        kanji = models.JMdictKanji(
            entry = entryObj, 
            content = self.getText(xml, 'keb'), 
            information = self.getText(xml, 'ke_inf'), 
            priorities = self.getList(xml, 'ke_pri')
        )
        kanji.save()
        return kanji
        
    def buildAndSaveReading(self, entryObj, xml):
        reading = models.JMdictReading(
            entry = entryObj, 
            content = self.getText(xml, 'reb'), 
            no_kanji = True if xml.find('re_nokanji') else False,
            restrictions = self.getText(xml, 're_restr'),
            information = self.getText(xml, 're_inf'),
            priorities = self.getList(xml, 're_pri')
        )
        reading.save()
        return reading

    def buildAndSaveSense(self, entryObj, xml):
        sense = models.JMdictSense(
            entry = entryObj,
            xreferences = self.getList(xml, 'xref'),
            antonyms = self.getList(xml, 'ant'),
            parts_of_speech = self.getList(xml, 'pos'),
            fields = self.getList(xml, 'field'),
            misc = self.getList(xml, 'misc'), 
            dialects = self.getList(xml, 'dial'),
            information = self.getText(xml, 's_inf')
        )
        sense.save()
        return sense

    def buildAndSaveGlossary(self, senseObj, xml):
        text, attrs = self.getTextWithAttributes(xml)
        glossary = models.JMdictGlossary(
            sense = senseObj, 
            gloss = text,
            language = attrs['lang'] if 'lang' in attrs else '',
            type = attrs['g_type'] if 'g_type' in attrs else ''
        )
        glossary.save()
        return glossary

    def buildAndSaveSource(self, senseObj, xml):
        text, attrs = self.getTextWithAttributes(xml)
        source = models.JMdictSource(
            sense = senseObj,
            content = text,
            language = attrs['lang'] if 'lang' in attrs else '',
            partial = True if 'ls_type' in attrs else False,
            waseieigo = True if 'ls_wasei' in attrs else False
        )
        source.save()
        return source

    def handle(self):
        printPercentages = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 100]
        
        tree = etree.parse(f'{PATH}')
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

                for jmGloss in jmSense.iter('gloss'):
                    self.buildAndSaveGlossary(senseKey, jmGloss)
                    stats[4] += 1

                for jmSource in jmSense.iter('lsource'):
                    self.buildAndSaveSource(senseKey, jmSource)
                    stats[5] += 1

            # TODO: better way
            percentComplete = round(100 * float(stats[4]) / TOTAL_GLOSSES)
            if percentComplete in printPercentages:
                printPercentages.remove(percentComplete)
                print(f'{str(percentComplete)}%')
    
        print(f'Entry:{stats[0]}, Kanji:{stats[1]}, Read:{stats[2]}, Sense:{stats[3]}, Gloss:{stats[4]}, Sour:{stats[5]}')
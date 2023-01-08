#!/usr/bin/env python

import os

from app import models


PATH = 'resources/'
INPUT = 'JMdict_e'

def between(ln, tag1, tag2):
    return ln.split(tag1)[1].split(tag2)[0]

def getCode(ln):
    return between(ln, '&', ';')

# code map used for parts of speech, fields and misc notes
codes = {}
# unique entry sequence id
entSeq = 0
# japanese readings typically including at least some kanji
kebs = []
# keb additional information one per keb
kebsInfs = {}
# keb priority (see jmdict) potentially multiple per keb
kebsPris = {}
# japanese readings primarily composed of kana
rebs = []
# reb additional information one per reb
rebsInfs = {}
# reb priority (see jmdict) potentially multiple per reb
rebsPris = {}
# parts of speech codes
poss = []
# field of application codes
fields = []
# misc. notes codes
miscs = []
# dialect codes
dials = []
# english translation with optional g_type
glosss = {}

edict2 = open(f'{PATH}/{INPUT}', 'r', encoding='utf-8')
for line in edict2:
    # strip trailing newline
    sln = line.strip()

    # temp values for individual readings
    currentKeb, currKebPris = '', []
    currentReb, currRebPris = '', []
    currentGloss, currGTypes = '', ''

    # build code dictionary
    if '<!ENTITY' in sln:
        # skipping the trailing " and >
        split = sln[0:len(sln) - 2].split(' ')
        code, name = split[1], split[2]
        codes[code] = name

    # elif '<entry>' in sln:

    elif '<ent_seq>' in sln:
        entSeq = int(between(sln, '<ent_seq>', '</ent_seq>'))

    elif '<keb>' in sln:
        keb = between(sln, '<keb>', '</keb>')
        kebs.append(keb)
        currentKeb = keb
        currKebPris = []

    elif '<ke_inf>' in sln:
        kebsInfs[keb] = getCode(sln)

    elif '<ke_pri>' in sln:
        currKebPris.append(getCode(sln))
        kebsPris[currentKeb] = currKebPris

    elif '<reb>' in sln:
        reb = between(sln, '<reb>', '</reb>')
        rebs.append(reb)
        currentReb = reb
        currRebPris = []

    elif '<re_pri>' in sln:
        currRebPris.append(getCode(sln))
        kebsPris[currentReb] = currRebPris
        
    elif '<sense>' in sln:
        poss, fields, miscs, dials = [], [], [], []
    elif '<pos>' in sln:
        poss.append(getCode(sln))

    elif '<field>' in sln:
        fields.append(getCode(sln))

    elif '<misc>' in sln:
        miscs.append(getCode(sln))

    elif '<dial>' in sln:
        dials.append(getCode(sln))

    elif '<gloss>' in sln:
        gloss = between(sln, '>', '</gloss>')
        gType = None
        if 'g_type=' in sln:
            gType = between(sln, '=\\"', '\\">')
        glosss[gloss] = gType
        
    
    

    # 
    elif '</entry>' in sln:
        kebs, rebs = {}, {}



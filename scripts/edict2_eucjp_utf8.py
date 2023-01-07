#!/usr/bin/env python

import os, codecs

INPUT = 'edict2'
OUTPUT = 'edict2_utf8.txt'
PATH = 'resources/'
GENERATED_PATH = 'resources/generated'

if os.path.exists(output_file):
    os.remove(output_file)

# EDICT2 file is distributed in JIS X 0208 and JIS X 0212 codings in EUC-JP encapsulation
# edict2 = open(f'{PATH}/{INPUT}}', 'r', encoding='JISX2013')
edict2 = codecs.open(f'{PATH}/{INPUT}', 'r', 'EUC-JP')
# edict2 = open(f'{PATH}/{INPUT}', 'rb')

count = 0
for line in edict2 and count < 10:
    print(line)
    count += 1

# with open(f'{GENERATED_PATH}/{OUTPUT}', 'w', encoding='utf-8') as edict_utf8:
#     for line in test:
#         edict_utf8.write(str(line))

#!/bin/bash

# seeds=$(find ./jpcore/management/commands/ -name "seed_*")
# seeds=$(grep -L 'seed_' ./jpcore/management/commands/ | awk 
# echo "$seeds"
for c in "seed_jmdict" "seed_krad" "seed_kanjidic"
do
    python3 manage.py "$c"
done

# JPCore
Read-only API for the JMDict EN-JP dictionary, KRAD/RADK associations, etc.

## Running Locally
1. Create env vars file with: \
`$ cp .env.example .env`
2. Apply migrations: \
`$ python3 manage.py migrate`
3. DB seed commands: \
`$ python3 manage.py [ seed_jmdict | seed_krad | seed_kanjidic ]`
4. Run DEVELOPMENT server: \
`$ python3 manage.py runserver`

## Manual Prod. Deploy
1. Set up local venv with: \
`$ python3 -m venv venv/`
2. Start python virtual environment with: \
`$ source venv/bin/activate`
3. Create .env using either: \
`$ cp .env.example .env` \
`$ printenv | sed 's/\([^=]*=\)\(.*\)/\1"\2"/' > .env`
4. Install dependencies with: \
`$ python3 -m pip install -r requirements.txt`
5. Invoke Gunicorn, pass Gunicorn config AND detach with: \
`$ nohup ./venv/bin/gunicorn -c gunicorn/prod.py &`
6. End venv session with: \
`$ deactivate`

## Running Tests
`$ python3 manage.py test`

## Manage.py Helpers
- Create model migration: \
`$ python3 manage.py makemigrations --name NAME GOES HERE`
- Unmigrate: \
`$ python3 manage.py migrate --fake jpcore zero`

## Scripts
- `clear_pycache.sh` - clear all Python bytecode caches
- `drop_tables.sh`   - destroy jpcore database
- `dl_radinfo.sh`    - download latest copy of jpcore's "Radicals" supplmentary data file 'resources/radinfo.tsv'

## Acknowledgements
- JMdict is copyright under the EDRDG licence see the [EDRDG wiki]((https://www.edrdg.org/wiki/index.php/)JMdict-EDICT_Dictionary_Project)) for more info.
- KRADFILE and RADKFILE files are copyright under the [EDRDG licence](http://www.edrdg.org/edrdg/licence.html). 
- strokeEditDistance and yehAndLiRadical CSVs are provided by Dr. Lars Yencken through his [website](https://lars.yencken.org/datasets/).

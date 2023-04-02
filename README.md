# JPCore
Read-only API for the JMDict EN-JP dictionary, KRAD/RADK associations, etc.

## Running Locally
1. Create env vars file with: \
`$ mv .env.example .env`
2. Apply migrations: \
`$ python3 manage.py migrate`
3. DB seed commands: \
`$ python3 manage.py seed_jmdict | seed_krad | seed_kanjidic ]`
4. Run DEVELOPMENT server: \
`$ python3 manage.py runserver`

## Manual Prod. Deploy
1. Set up local venv with: \
`$ python3 -m venv venv/`
2. Start python virtual environment with: \
`$ source venv/bin/activate`
3. Install dependencies with: \
`$ python3 -m pip install -r requirements.txt`
4. Create .env using either: \
`$ cp .env.example .env` \
`$ printenv | sed 's/\([^=]*=\)\(.*\)/\1"\2"/' > .env`
5. Install [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) and configure to listen on port 443 and reroute accordingly
6. Install and use [mkcert](https://github.com/FiloSottile/mkcert) to install a self-signed cert for nginx using [this](https://www.howtoforge.com/how-to-create-locally-trusted-ssl-certificates-with-mkcert-on-ubuntu/)
7. Create Gunicorn socket and config nginx to use it following [this](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04#step-6-testing-gunicorn-s-ability-to-serve-the-project) guide
8. Start Gunicorn server AND detach with: \
`$ nohup sh scripts/start_server.sh &`
9. End venv session with: \
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
- `start_server.sh`  - configured Gunicorn server start

## Acknowledgements
- JMdict is copyright under the EDRDG licence see the [EDRDG wiki]((https://www.edrdg.org/wiki/index.php/)JMdict-EDICT_Dictionary_Project)) for more info.
- KRADFILE and RADKFILE files are copyright under the [EDRDG licence](http://www.edrdg.org/edrdg/licence.html). 
- strokeEditDistance and yehAndLiRadical CSVs are provided by Dr. Lars Yencken through his [website](https://lars.yencken.org/datasets/).

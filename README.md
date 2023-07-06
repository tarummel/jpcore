# JPCore
Read-only API for the JMDict EN-JP dictionary, KRAD/RADK associations, etc.

## External Dependencies
Install [Docker](https://docs.docker.com/get-docker/) \
Install [Memcached](https://memcached.org/) \
Install [PostgresSQL](https://www.postgresql.org/download/)

## Running Locally
1. Create env vars file: \
`$ cp .env.example .env`
2. Apply migrations: \
`$ python3 manage.py migrate`
3. DB seed commands: \
`$ python3 manage.py [ seed_all | seed_jmdict | seed_krad | seed_kanjidic ]`
4. Run DEVELOPMENT server: \
`$ python3 manage.py runserver`

## Docker-Compose Locally
Start/stop everything: \
`$ docker-compose [up|down]` \
Run a specific service: \
`$ docker-compose up psql` \
Detach with `--detach`: \
`$ docker-compose up -d` \
Clear unused content: \
`$ docker system prune`

## Running Tests
`$ python3 manage.py test`

## manage.py Helpers
- Create model migration: \
`$ python3 manage.py makemigrations --name NAME GOES HERE`
- Unmigrate: \
`$ python3 manage.py migrate --fake jpcore zero`

## Scripts
- `clear_pycache.sh` - clear all Python bytecode caches
- `drop_tables.sh`   - destroy jpcore database
- `dl_radinfo.sh`    - download latest copy of jpcore's "Radicals" model file to 'resources/radinfo.tsv'

## Acknowledgements
- kradfile, radkfile, JMdict_e and kanjidic2 are copyright under the [EDRDG licence](http://www.edrdg.org/edrdg/licence.html). 
- strokeEditDistance and yehAndLiRadical CSVs are provided by Dr. Lars Yencken through his [website](https://lars.yencken.org/datasets/).

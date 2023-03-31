#!/bin/bash

# AWS Code Deploy 'BeforeInstall' step, see: appspec.yml

cd /home/admin/www/project/

# Start venv
python3 -m venv venv/
source venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt

# Dump env vars
rm .env
printenv | sed 's/\([^=]*=\)\(.*\)/\1"\2"/' > .env

# do this after running app not before
# deactivate

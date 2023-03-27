#!/bin/bash

cd /home/ec2-user/www/project/

# Install dependencies
pip install -r requirements.txt

# Dump env vars
rm .env
printenv | sed 's/\([^=]*=\)\(.*\)/\1"\2"/' > .env

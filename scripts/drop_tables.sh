#!/bin/bash

dbname='jpcore'
dbs=$(psql -d ${dbname} -c "\d" | grep "jpcore_" | awk '{print $3}')
for db in $dbs
do
  echo $db
  psql -d "$dbname" -c "DROP TABLE ${db} CASCADE"
done

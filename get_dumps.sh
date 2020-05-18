#!/usr/bin/env bash

mkdir -p ./dumps

docker exec mysql sh -c 'exec mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" users_db' > ./dumps/dump.sql
# only while docker is active!

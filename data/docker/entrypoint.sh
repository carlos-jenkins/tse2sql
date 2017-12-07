#!/usr/bin/env bash

set -o errexit
set -o nounset

###############
# Supervisord #
###############

supervisord -c /etc/supervisor/supervisord.conf

###############
# MySQL       #
###############

# Wait for MySQL to start
echo -n "Waiting for MySQL"
for i in {30..0}; do
    if mysqladmin ping >/dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 1
done
echo ""

if [ "$i" == 0 ]; then
    echo >&2 'FATAL: MySQL failed to start'
    exit 1
fi


###############
# MongoDB     #
###############

# Wait for mongod
echo -n "Waiting for mongod"
while ! mongo --eval "db.version()" > /dev/null 2>&1; do
    echo -n "."; sleep 0.2
done
echo ""


exec "$@"

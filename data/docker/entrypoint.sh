#!/usr/bin/env bash

set -o errexit
set -o nounset

###############
# Supervisord #
###############

# Workaround for issue #72 that makes MySQL to fail to
# start when using docker's overlay2 storage driver:
#   https://github.com/docker/for-linux/issues/72
sudo find /var/lib/mysql -type f -exec touch {} \;

sudo supervisord -c /etc/supervisor/supervisord.conf

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
    echo "Showing content of /var/log/mysql/error.log ..."
    cat /var/log/mysql/error.log || true
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


echo "Finished initialization ..."
exec "/bin/bash"

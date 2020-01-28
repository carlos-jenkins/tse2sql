#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

echo "===== INITIALIZING ====="

echo "DATA_HASH: ${DATA_HASH}"
echo "TIMESTAMP: ${TIMESTAMP}"

echo -n "Waiting for MySQL"
for i in {30..0}; do
    if mysqladmin ping -hdb --silent; then
        break
    fi
    echo -n "."
    sleep 1
done
echo ""


echo "===== IMPORTING DATA ====="

echo "Extraction processed data ..."
mkdir wstmp
pushd wstmp

tar -zxvf "../ws/csv/${DATA_HASH}/${DATA_HASH}.tar.gz"
tar -zxvf "../ws/web/${TIMESTAMP}/${TIMESTAMP}.tar.gz"


echo "Importing CSV data into database ..."
echo "
    SET @start := NOW();
    source ${DATA_HASH}.mysql.sql;
    SET @end := NOW();
    SELECT TIMEDIFF(@end, @start);
" | mysql --host=db --user=root


echo "Importing WEB data into database ..."
echo "
    SET @start := NOW();
    source ${TIMESTAMP}.scrapped.mysql.sql;
    SET @end := NOW();
    SELECT TIMEDIFF(@end, @start);
" | mysql --host=db --user=root

popd


echo "===== NORMALIZING ====="

mkdir -p "ws/ready/${DATA_HASH}+${TIMESTAMP}"
pushd "ws/ready/${DATA_HASH}+${TIMESTAMP}"


echo "Assigning code to voters ..."
echo "
    SET @start := NOW();
    USE tse2sql;
    CALL ASSIGN_CODES();
    SET @end := NOW();
    SELECT TIMEDIFF(@end, @start);
" | mysql --host=db --user=root

echo "Exporting normalized database for archival ..."
mysqldump --host=db --user=root tse2sql |
    gzip > "${DATA_HASH}+${TIMESTAMP}.normalized.mysql.sql.gz"


echo "===== DENORMALIZING ====="

echo "Denormalizing database ..."
echo "
    SET @start := NOW();
    USE tse2sql;
    CALL DENORMALIZE_DB();
    SET @end := NOW();
    SELECT TIMEDIFF(@end, @start);
" | mysql --host=db --user=root

echo "Exporting denormalized database for archival ..."
mysqldump --host=db --user=root tse2sql denormalized |
    gzip > "${DATA_HASH}+${TIMESTAMP}.denormalized.mysql.sql.gz"


popd

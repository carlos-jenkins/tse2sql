#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

SOURCE_URL=https://www.tse.go.cr/zip/padron/padron_completo.zip
ARCHIVE_URL="https://archive.kuralabs.io/mivotico/tse2sql/$(date +%Y)"

echo "===== CHECK FORCE MODE ====="

FORCE_DATA_HASH=${FORCE_DATA_HASH:-}
FORCE_TIMESTAMP=${FORCE_TIMESTAMP:-}

echo "FORCE_DATA_HASH: ${FORCE_DATA_HASH}"
echo "FORCE_TIMESTAMP: ${FORCE_TIMESTAMP}"

if [ -n "${FORCE_DATA_HASH}" ] && [ -n "${FORCE_TIMESTAMP}" ]; then

    echo "Both forced DATA_HASH and TIMESTAMP were provided. Downloading from archive ..."
    mkdir -p "ws/csv/${FORCE_DATA_HASH}"
    mkdir -p "ws/web/${FORCE_TIMESTAMP}"
    pushd ws

    CSV_ARCHIVE="csv/${FORCE_DATA_HASH}/${FORCE_DATA_HASH}.tar.gz"
    curl --output "${CSV_ARCHIVE}" "${ARCHIVE_URL}/${CSV_ARCHIVE}"

    WEB_ARCHIVE="web/${FORCE_TIMESTAMP}/${FORCE_TIMESTAMP}.tar.gz"
    curl --output "${WEB_ARCHIVE}" "${ARCHIVE_URL}/${WEB_ARCHIVE}"

    echo "Recording input identifiers ..."
    echo "{\"sha256\": \"${FORCE_DATA_HASH}\", \"timestamp\": \"${FORCE_TIMESTAMP}\"}" |
        python3 -m json.tool > latest.json

    echo "Final data for archiving:"
    tree

    popd
    exit 0
fi


echo "===== INITIALIZING ====="

echo "Installing tse2sql ..."
python3 setup.py bdist_wheel
sudo pip3 install dist/tse2sql-*.whl

echo "Checking tse2sql installation ..."
tse2sql --help

mkdir ws
pushd ws


echo "===== CSV DATA SOURCE PROCESSING ====="

mkdir csv
pushd csv

echo "Downloading currently published electoral registry from ${SOURCE_URL} ..."
curl --output padron.zip "${SOURCE_URL}"

echo "Calculating data hash ..."
DATA_HASH=$(sha256sum --binary padron.zip | cut -d' ' -f 1)
echo "Hash (sha256) of the archive downloaded : ${DATA_HASH}"

mkdir "${DATA_HASH}"
pushd "${DATA_HASH}"

echo "Checking archive for ${DATA_HASH} ..."
ARCHIVED_REGISTRY="${ARCHIVE_URL}/csv/${DATA_HASH}/${DATA_HASH}.tar.gz"
DATA_AVAILABLE=$(curl --silent --head "${ARCHIVED_REGISTRY}" | grep "404 Not Found" || true)

if [ -z "${DATA_AVAILABLE}" ]; then

    echo "Data source ${DATA_HASH} already processed. Will use archived results."

    echo "Removing source data ..."
    rm ../padron.zip

    echo "Downloading archived results from ${ARCHIVED_REGISTRY} ..."
    curl --output "${DATA_HASH}.tar.gz" "${ARCHIVED_REGISTRY}"

    echo "Extracting archived results from ${DATA_HASH}.tar.gz ..."
    tar -zxvf "${DATA_HASH}.tar.gz"

else

    echo "New data source ${DATA_HASH}. Processing ..."

    mv ../padron.zip "${DATA_HASH}.zip"
    tse2sql "${DATA_HASH}.zip"

    echo "Compressing generated data for archival ..."
    tar -zcvf \
        "${DATA_HASH}.tar.gz" \
        "${DATA_HASH}.mysql.sql" \
        "${DATA_HASH}.data.json" \
        "${DATA_HASH}.samples.json"

    echo "Removing source data ..."
    rm -r "${DATA_HASH}" "${DATA_HASH}.zip"
fi

popd
popd


echo "===== WEB DATA SOURCE PROCESSING ====="

mkdir web
pushd web

TIMESTAMP=$(date +%s)
echo "Timestamp identifier for this session : ${TIMESTAMP} ..."

mkdir "${TIMESTAMP}"
pushd "${TIMESTAMP}"

echo "Using ${DATA_HASH}.samples.json for this session. Renaming ..."
cp "../../csv/${DATA_HASH}/${DATA_HASH}.samples.json" \
    "${TIMESTAMP}.samples.json"

echo "Starting scrapper using ${DATA_HASH}.samples.json ..."
tse2sql-scrapper "${TIMESTAMP}.samples.json"

echo "Recording input identifiers ..."
echo "{\"sha256\": \"${DATA_HASH}\", \"timestamp\": \"${TIMESTAMP}\"}" |
    python3 -m json.tool > "${TIMESTAMP}.input.json"

echo "Compressing generated data for archival ..."
tar -zcvf \
    "${TIMESTAMP}.tar.gz" \
    "${TIMESTAMP}.input.json" \
    "${TIMESTAMP}.unscrapped.json" \
    "${TIMESTAMP}.scrapped.mysql.sql"

echo "Removing samples file ..."
rm "${TIMESTAMP}.samples.json"

popd
popd


echo "===== PREPARING DATA ARCHIVE ====="

echo "Tree before cleaning up:"
tree

echo "Cleaning up workspace ..."
mv "web/${TIMESTAMP}/${TIMESTAMP}.input.json" latest.json

rm "csv/${DATA_HASH}/${DATA_HASH}.data.json"
rm "csv/${DATA_HASH}/${DATA_HASH}.samples.json"
rm "csv/${DATA_HASH}/${DATA_HASH}.mysql.sql"

rm "web/${TIMESTAMP}/${TIMESTAMP}.unscrapped.json"
rm "web/${TIMESTAMP}/${TIMESTAMP}.scrapped.mysql.sql"


echo "Final data for archiving:"
tree

popd
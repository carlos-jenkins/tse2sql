#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Jenkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Very basic Rest API example implemented in Python-Flask.
"""

from json import loads
from datetime import datetime, date
from os.path import abspath, dirname, join

from pymysql import connect, cursors
from flask.json import JSONEncoder
from flask import Flask, abort, jsonify, make_response


VOTER_BY_ID_QUERY = (
    'SELECT id_voter, name, family_name_1, family_name_2, sex, '
    'id_expiration, name_province, name_canton, name_district, site '
    'FROM voter '
    'JOIN district ON voter.district_id_district = district.id_district '
    'JOIN canton ON district.canton_id_canton = canton.id_canton '
    'JOIN province ON canton.province_id_province = province.id_province '
    'WHERE voter.id_voter = %s;'
)

VOTER_BY_NAME_QUERY = (
    'SELECT * FROM voter '
    'WHERE MATCH(name, family_name_1, family_name_2) '
    'AGAINST (%s IN BOOLEAN MODE) LIMIT 30;'
)

DB_MIN_TOKEN_SIZE = 3


class DatesJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date) or isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


with open(join(dirname(abspath(__file__)), 'settings.json')) as fd:
    config = loads(fd.read())

db = connect(
    host=config.get('host', 'localhost'),
    user=config.get('user', 'tsesql'),
    password=config.get('password', ''),
    db=config.get('db', 'tsesql'),
    charset='utf8mb4',
    cursorclass=cursors.DictCursor
)
app = Flask('tsesql', static_folder=None)
app.json_encoder = DatesJSONEncoder


@app.route('/voter/info-by-id/<int:voter_id>', methods=['GET'])
def info_by_id(voter_id):
    with db.cursor() as cursor:
        cursor.execute(VOTER_BY_ID_QUERY, (voter_id, ))
        result = cursor.fetchone()
    return jsonify(result)


@app.route('/voter/info-by-name/<voter_name>', methods=['GET'])
def info_by_name(voter_name):
    if not voter_name:
        abort(400)

    prepared = ' '.join([
        '+{}'.format(token)
        if len(token) >= DB_MIN_TOKEN_SIZE
        else token
        for token in voter_name.split()
    ])

    with db.cursor() as cursor:
        cursor.execute(VOTER_BY_NAME_QUERY, (prepared, ))
        result = cursor.fetchall()
    return jsonify(results=result)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(
        port=config.get('api_port', 5000),
        debug=True
    )

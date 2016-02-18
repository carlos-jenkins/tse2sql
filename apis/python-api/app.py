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


BASE_QUERY = (
    'SELECT id_voter, name, family_name_1, family_name_2, sex, '
    'id_expiration, name_province, name_canton, name_district, site '
    'voting_center_name, voting_center_address, '
    'voting_center_latitude, voting_center_longitude '
    'FROM voter '
    'JOIN district ON voter.district_id_district = district.id_district '
    'JOIN canton ON district.canton_id_canton = canton.id_canton '
    'JOIN province ON canton.province_id_province = province.id_province '
)

VOTER_BY_ID_QUERY = (
    BASE_QUERY +
    'WHERE voter.id_voter = %s;'
)

VOTER_BY_NAME_QUERY = (
    BASE_QUERY +
    'WHERE MATCH(name, family_name_1, family_name_2) '
    'AGAINST (%s IN BOOLEAN MODE) LIMIT 30;'
)

DB_MIN_TOKEN_SIZE = 3


class DatesJSONEncoder(JSONEncoder):
    """
    Custom JSONEncoder class that knows how to serialize Python date types.
    """
    def default(self, obj):
        # No real use here, just make sure this is the backend encoder
        import simplejson  # noqa

        try:
            if isinstance(obj, date) or isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class TseSqlApp(object):
    """
    Tse2Sql Python-Flask REST API example.
    """

    def __init__(self, ):

        # Read configuration
        with open(join(dirname(abspath(__file__)), 'settings.json')) as fd:
            self.config = loads(fd.read())

        # Create database connection
        self.db = connect(
            host=self.config.get('host', 'localhost'),
            user=self.config.get('user', 'tsesql'),
            password=self.config.get('password', ''),
            db=self.config.get('db', 'tsesql'),
            charset='utf8mb4',
            cursorclass=cursors.DictCursor
        )

        # Configure Flask application
        self.app = Flask('tsesql', static_folder=None)
        self.app.json_encoder = DatesJSONEncoder
        # self.app.errorhandler(404)(self.not_found)

        # Define routes
        routes = [
            ('/voter/info-by-id/<int:voter_id>', self.info_by_id),
            ('/voter/info-by-name/<voter_name>', self.info_by_name)
        ]
        for endpoint, method in routes:
            self.app.route(endpoint, methods=['GET'])(method)

    def info_by_id(self, voter_id):
        """
        Get a voter by voter id.

        :param int voter_id: Voter identity card number.
        """
        # Adapt 7 digits ids
        # PAAABBB -> P0AAA0BBB
        if voter_id < 10000000:
            voter_id = (
                ((voter_id // 1000000) * 100000000) +
                (((voter_id // 1000) % 1000) * 10000) +
                (voter_id % 1000)
            )

        with self.db.cursor() as cursor:
            cursor.execute(VOTER_BY_ID_QUERY, (voter_id, ))
            result = cursor.fetchone()

        if result is None:
            abort(404)

        return jsonify(result)

    def info_by_name(self, voter_name):
        """
        Get a voter by name.

        :param str voter_name: Name of the voter to look for.
        """
        if not voter_name:
            abort(400)

        prepared = ' '.join([
            '+{}'.format(token)
            if len(token) >= DB_MIN_TOKEN_SIZE
            else token
            for token in voter_name.split()
        ])

        with self.db.cursor() as cursor:
            cursor.execute(VOTER_BY_NAME_QUERY, (prepared, ))
            result = cursor.fetchall()
        return jsonify(results=result)

    def not_found(self, error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def run(self):
        self.app.run(
            port=self.config.get('api_port', 5000),
            debug=True
        )


if __name__ == '__main__':
    app = TseSqlApp()
    app.run()

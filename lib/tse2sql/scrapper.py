# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 KuraLabs S.R.L
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
TSE voting center data scrapper module.
"""

from time import sleep
from json import dumps
from logging import getLogger
from traceback import format_exc
from collections import OrderedDict

from tqdm import tqdm
from requests import post
from inflection import titleize, humanize
from urllib.parse import urlparse, parse_qs


log = getLogger(__name__)


SCRAPPER_URL = (
    'http://www.tse.go.cr/dondevotarp/prRemoto.aspx/ObtenerDondeVotar'
)


def parse_location(url):
    """
    Parse latitude and longitude from a Google Maps URL.
    """
    params = parse_qs(urlparse(url).query, keep_blank_values=True)
    if 'll' in params:
        return tuple(float(c) for c in params.get('ll')[0].split(','))
    return (0.0, 0.0)


def scrappe_data(samples):
    """
    Scrapper main function.

    :param dict samples: A dictionary with the ids samples.
    :return: A dictionary with the scrapped data of the form.
    :rtype: dict
    """

    headers = {'Content-Type': 'application/json'}
    scrapped_data = OrderedDict()
    unscrapped_data = OrderedDict()

    with tqdm(
        total=len(samples), unit='r', ascii=True, leave=True,
        desc='POST requests'
    ) as pbar:

        # Iterate samples to grab data from web service
        for district, voters_ids in samples.items():

            num_sample_voters = len(voters_ids)

            retries = 10
            while retries > 0:

                id_voter = voters_ids[retries % num_sample_voters]
                payload = dumps({'numeroCedula': str(id_voter)})

                try:
                    response = post(
                        SCRAPPER_URL,
                        headers=headers,
                        data=payload
                    )
                    response.raise_for_status()

                    data = response.json()['d']['lista']

                    latitude, longitude = parse_location(data['url'])
                    address = humanize(
                        data['direccionEscuela'].strip().lower()
                    )
                    name = titleize(
                        data['nombreCentroVotacion'].strip().lower()
                    )

                    # Record data
                    scrapped_data[district] = {
                        'latitude': latitude,
                        'longitude': longitude,
                        'address': address,
                        'name': name
                    }

                    pbar.update(1)
                    break
                except Exception:
                    log.error(
                        'Error while processing district #{} '
                        'using voter id #{} :: (RETRIES LEFT: {})'.format(
                            district, id_voter, retries
                        )
                    )
                    log.debug(format_exc())
                    sleep(10)

                retries -= 1

            else:
                log.error(
                    'Unable to get data for district #{} using {}'.format(
                        district, voters_ids
                    )
                )
                unscrapped_data[district] = voters_ids

    return scrapped_data, unscrapped_data


__all__ = ['scrappe_data']

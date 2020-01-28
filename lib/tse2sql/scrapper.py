# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2018 KuraLabs S.R.L
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
from urllib.parse import urlparse, parse_qs
from collections import OrderedDict, Counter

from tqdm import tqdm
from requests import Session
from inflection import titleize, humanize


log = getLogger(__name__)


SCRAPPER_URL = (
    'https://www.tse.go.cr/dondevotarM/prRemoto.aspx/ObtenerDondeVotar'
)


def parse_location(url):
    """
    Parse latitude and longitude from a Google Maps URL.

    URL is in the form:

        https://maps.google.com/maps/ms?...&ll=9.029795,-83.299043&...

    Sometimes there is a weird ll query param like this:

        https://maps.google.com/maps/ms?...&ll=9.029795, -83.299043,255&...
    """
    params = parse_qs(urlparse(url).query, keep_blank_values=True)
    if 'll' in params:
        return tuple(float(c) for c in params.get('ll')[0].split(','))[0:2]
    return (0.0, 0.0)


def scrappe_data(samples):
    """
    Scrapper main function.

    :param dict samples: A dictionary with the id_site to ids samples map.

    :return: A dictionary with the scrapped data of the form.
    :rtype: dict
    """

    session = Session()

    headers = {'Content-Type': 'application/json'}
    scrapped_data = OrderedDict()
    unscrapped_data = OrderedDict()

    voting_centers_per_district = Counter()

    with tqdm(
        total=len(samples), unit='r', ascii=True, leave=True,
        desc='POST requests'
    ) as pbar:

        # Iterate samples to grab data from web service
        for id_key in sorted(samples.keys()):

            id_site = int(id_key)
            voters_ids = samples[id_key]
            num_sample_voters = len(voters_ids)

            retries = 10
            while retries > 0:

                id_voter = voters_ids[retries % num_sample_voters]
                payload = dumps({'numeroCedula': str(id_voter)})

                try:
                    response = session.post(
                        SCRAPPER_URL,
                        headers=headers,
                        data=payload
                    )
                    response.raise_for_status()

                    data = response.json()['d']['lista']

                    # Check data
                    assert data
                    assert data['junta'] == id_site

                    # Fetch data
                    id_district = data['codElectoral']

                    name = titleize(
                        data['nombreCentroVotacion'].strip().lower()
                    )
                    address = humanize(
                        data['direccionEscuela'].strip().lower()
                    )

                    # Check for varchar overflow
                    if len(name) > 100:
                        log.warning(
                            'Name will overflow the column '
                            '"name": {}'.format(name)
                        )
                    if len(address) > 100:
                        log.warning(
                            'Name will overflow the column '
                            '"address": {}'.format(address)
                        )

                    latitude, longitude = parse_location(data['url'])

                    # Record data
                    unique = (id_district, name)
                    if unique not in scrapped_data:

                        # New voting center
                        voting_centers_per_district[id_district] += 1
                        id_voting_center = (id_district * 1000) + \
                            voting_centers_per_district[id_district]

                        scrapped_data[unique] = {
                            'id_voting_center': id_voting_center,
                            'id_sites': [id_site],
                            'address': address,
                            'latitude': latitude,
                            'longitude': longitude,
                        }
                    else:
                        scrapped_data[unique]['id_sites'].append(id_site)

                    pbar.update(1)
                    break
                except Exception:
                    log.error(
                        'Error while processing site #{} '
                        'using voter id #{} :: (RETRIES LEFT: {})'.format(
                            id_site, id_voter, retries
                        )
                    )
                    log.error(format_exc())
                    sleep(10)

                retries -= 1

            else:
                log.error(
                    'Unable to get data for site #{} using {}'.format(
                        id_site, voters_ids
                    )
                )
                unscrapped_data[id_site] = voters_ids

    return scrapped_data, unscrapped_data


__all__ = ['scrappe_data']

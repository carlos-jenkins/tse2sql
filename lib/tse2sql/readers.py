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
TSE files parsing / reading module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import listdir
from logging import getLogger
from traceback import format_exc
from os.path import abspath, join
from collections import OrderedDict
from codecs import open as open_with_encoding

from inflection import titleize


log = getLogger(__name__)


VOTERS_FILE = 'padron_completo.txt'


def get_file(search_dir, filename):
    """
    Get file asdas
    """
    filematch = filename.lower()

    for fnm in listdir(search_dir):
        if fnm.lower() == filematch:
            return abspath(join(search_dir, fnm))

    raise Exception('No such file: {}'.format(filename))


class DistrictsReader(object):
    """
    Read and parse the ``Distelec.txt`` file.

    The ``Distelec.txt`` file is a CSV file in the form:

    ::

        101001,SAN JOSE,CENTRAL,HOSPITAL
        101002,SAN JOSE,CENTRAL,ZAPOTE
        101003,SAN JOSE,CENTRAL,SAN FRANCISCO DE DOS RIOS
        101004,SAN JOSE,CENTRAL,URUCA
        101005,SAN JOSE,CENTRAL,MATA REDONDA
        101006,SAN JOSE,CENTRAL,PAVAS

    - It list the provinces, cantons and districts of Costa Rica.
    - It is encoded in ``ISO-8859-15`` and uses Windows CRLF line terminators.
    - It is quite stable. It will only change when Costa Rica districts change
      (quite uncommon, but happens from time to time).
    - It is relatively small. Costa Rica has 81 cantons, and ~6 or so
      districts per canton. As of 2016, Costa Rica has 478 districts.
      As this writting, the CSV file is 172KB in size.
    - The semantics of the code is as following:

      ::

          <province(1 digit)><canton(2 digits)><district(3 digits)>

    This class will lookup for the file and will process it completely in main
    memory in order to build provinces, cantons and districts tables at the
    same time. Also, the file will be processed even if some lines are
    malformed. Any error will be logged as such.
    """

    def __init__(self, search_dir):
        self._search_dir = search_dir
        self._filename = get_file(search_dir, 'Distelec.txt')
        self.provinces = OrderedDict()
        self.cantons = OrderedDict()
        self.districts = OrderedDict()

    def parse(self):
        """
        """
        with open_with_encoding(self._filename, 'rb', 'iso8859-15') as fd:
            for linenum, line in enumerate(fd):
                line = line.strip()
                try:
                    parts = line.split(',')
                    assert len(parts) == 4

                    # Get codes
                    code = int(parts[0])

                    # Insert province
                    province_code = code // 100000
                    province_name = titleize(parts[1].strip())

                    if province_code in self.provinces:
                        assert self.provinces[province_code] == province_name
                    else:
                        self.provinces[province_code] = province_name

                    # Insert canton
                    canton_code = (
                        province_code,
                        (code % 100000) // 1000
                    )
                    canton_name = titleize(parts[2].strip())

                    if canton_code in self.cantons:
                        assert self.cantons[canton_code] == canton_name
                    else:
                        self.cantons[canton_code] = canton_name

                    # Insert district
                    district_code = (
                        canton_code,
                        code % 1000
                    )
                    district_name = titleize(parts[3].strip())
                    if district_code in self.districts:
                        assert self.districts[district_code] == district_name
                    else:
                        self.districts[district_code] = district_name

                except Exception:
                    log.error(
                        'Distelec.txt :: Bad data at line #{}'.format(
                            linenum, line
                        )
                    )
                    log.debug(format_exc())
                    continue


class VotersReader(object):
    """
    Read and parse the ``PADRON_COMPLETO.txt`` file.

    The ``PADRON_COMPLETO.txt`` file is a CSV file in the form:

    ::

        100339724,109007,1,20231119,01031,JOSE                          ,DELGADO                   ,CORRALES
        100429200,109006,2,20221026,01025,PAULA                         ,QUIROS                    ,QUIROS
        100697455,101023,2,20150620,00073,CARMEN                        ,FALLAS                    ,GUEVARA
        100697622,101020,2,20230219,00050,ANTONIA                       ,RAMIREZ                   ,CARDENAS
        100720641,108002,2,20241119,00884,SOLEDAD                       ,SEQUEIRA                  ,MORA
        100752764,403004,1,20151208,03731,EZEQUIEL                      ,LEON                      ,CALVO
        100753244,210012,2,20161009,02599,CONSTANCIA                    ,ARIAS                     ,RIVERA
        100753335,115001,2,20180211,01362,MARGARITA                     ,ALVARADO                  ,LAHMAN
        100753618,111005,2,20220109,01168,ETELVINA                      ,PARRA                     ,SALAZAR
        100763791,108007,1,20190831,00971,REINALDO                      ,MENDEZ                    ,BARBOZA

    - It lists all the voters in Costa Rica, ... FIXME
    - It is encoded in ``ISO-8859-15`` and uses Windows CRLF line terminators.
    """  # noqa

    def __init__(self, search_dir):
        super(VotersReader, self).__init__(VOTERS_FILE, search_dir)


__all__ = ['DistrictsReader', 'VotersReader']

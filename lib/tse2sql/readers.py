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
from os.path import abspath, join


log = getLogger(__name__)


DISTRICTS_FILE = 'distelec.txt'
VOTERS_FILE = 'padron_completo.txt'


class FileReader(object):
    """
    """
    def __init__(self, filename, search_dir, encoding='utf-8'):
        self._filename = None
        self._fd = None

        # Search for file
        for fnm in listdir(search_dir):
            if fnm.lower() == filename:
                self._filename = abspath(join(search_dir, fnm))
                break
        else:
            raise Exception(
                'No such file {}'.format(filename)
            )

    def __enter__(self):
        self._fd = open(self._filename, 'rb')
        return self

    def __exit__(self, type, value, traceback):
        if self._fd:
            self._fd.close()

    def __iter__(self):
        return self

    def __next__(self):
        next()


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

    It is encoded in ``ISO-8859-15`` and uses Windows CRLF line terminators.
    """

    def __init__(self, search_dir):
        super(DistrictsReader, self).__init__(DISTRICTS_FILE, search_dir)


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

    It is encoded in ``ISO-8859-15`` and uses Windows CRLF line terminators.
    """  # noqa

    def __init__(self, search_dir):
        super(VotersReader, self).__init__(VOTERS_FILE, search_dir)


__all__ = ['DistrictsReader', 'VotersReader']

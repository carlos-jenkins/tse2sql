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
SQL rendering module.
"""

from logging import getLogger
from collections import OrderedDict

from .renderers.mysql import write_mysql, write_mysql_scrapper


log = getLogger(__name__)


RENDERERS = OrderedDict([
    ('mysql', (write_mysql, write_mysql_scrapper))
])


def list_renderers():
    """
    List availables templates.

    :return: The list of available templates.
    :rtype: list
    """
    return RENDERERS.keys()


def render(payload, renderer, sqlfile):
    """
    Render given payload using given renderer.

    :param dict payload: The payload to render.
    :param str renderer: The name of the renderer to use.
    :param file sqlfile: Output file descriptor to write to.
    """
    RENDERERS[renderer][0](sqlfile, payload)


def render_scrapped(data, renderer, sqlfile):
    """
    Render given payload using given renderer.

    :param dict data: The scrapped data to render.
    :param str renderer: The name of the renderer to use.
    :param file sqlfile: Output file descriptor to write to.
    """
    RENDERERS[renderer][1](sqlfile, data)


__all__ = ['list_renderers', 'render', 'render_scrapped']

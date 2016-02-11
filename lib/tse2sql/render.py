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
SQL rendering module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from pkgutil import get_data
from logging import getLogger

from jinja2 import Environment, FunctionLoader, StrictUndefined


log = getLogger(__name__)


def list_templates():
    """
    List availables templates.

    :return: The list of available templates.
    :rtype: list
    """
    from os import listdir
    from sys import modules
    from os.path import dirname, join, splitext
    directory = join(dirname(modules['tse2sql'].__file__), 'templates')
    templates = sorted([
        name for name, ext in [splitext(fn) for fn in listdir(directory)]
        if ext == '.tpl'
    ])
    return templates


def render(template, payload):
    """
    Render given template with given payload.

    :param str template: The name of the template.
    :param dict payload: The payload to render the template with.
    :rtype: str
    :return: The rendered template.
    """
    def load_template(name):
        return get_data(
            'tse2sql', 'templates/{}.tpl'.format(name)
        ).decode('utf-8')

    env = Environment(
        loader=FunctionLoader(load_template),
        undefined=StrictUndefined
    )

    raw_tpl = env.get_template(template)
    return raw_tpl.render(**payload)

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
Utilities module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os import makedirs
from logging import getLogger
from hashlib import sha256 as sha256lib
from os.path import basename, splitext, join
from tempfile import NamedTemporaryFile, gettempdir

from tqdm import tqdm
from requests import get


log = getLogger(__name__)


def ensure_dir(path):
    """
    Ensure that a path exists.

    :param str path: Directory path to create.
    """
    import errno
    EEXIST = getattr(errno, 'EEXIST', 0)  # noqa

    try:
        makedirs(path)
    except OSError as err:
        # 0 for Jython/Win32
        if err.errno not in [0, EEXIST]:
            raise


def download(url, subdir=None):
    """
    Download given file in system temporal files folder.

    :param str url: URL of the file to download.
    :param str subdir: Subfolder name to store the downloaded file in the
     system temporal files folder.
    :return: Local path where the file was stored.
    :rtype: str
    """
    log.info('Attempting to download file: {}'.format(url))
    response = get(url, stream=True)
    size = int(response.headers['content-length'])
    log.info('File is {:.2f} MBs long, downloading...'.format(size / 1000000))

    name, ext = splitext(basename(url))
    directory = gettempdir()
    if subdir is not None:
        directory = join(directory, subdir)

    ensure_dir(directory)

    tmpopts = {
        'mode': 'w+b',
        'suffix': ext,
        'prefix': name + '_',
        'dir': directory,
        'delete': False
    }
    total = 0
    with NamedTemporaryFile(**tmpopts) as fd:
        with tqdm(total=size, unit='B', unit_scale=True) as pbar:
            for data in response.iter_content():
                chunk = len(data)
                total += chunk
                pbar.update(chunk)
                fd.write(data)

    log.info(
        'Done. File saved in {} ({:.2f})MBs'.format(
            fd.name, total / 1000000
        )
    )
    return fd.name


def sha256(filename, chunk_size=2**10):
    """
    Calculate SHA256 of given filename.

    :param str filename: Filename to calculate SHA256 from.
    :param int chunk_size: Maximum size of the buffer used to read the file.
    :return: SHA256 hexidecimal digest.
    :rtype: str
    """
    sha = sha256lib()

    with open(filename, 'rb') as fd:
        while True:
            block = fd.read(chunk_size)
            if not block:
                break
            sha.update(block)

    return sha.hexdigest()

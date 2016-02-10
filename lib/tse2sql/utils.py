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
from zipfile import ZipFile
from logging import getLogger
from hashlib import sha256 as sha256lib
from tempfile import NamedTemporaryFile, gettempdir
from os.path import basename, abspath, splitext, join

from six.moves.urllib.parse import urlparse

from tqdm import tqdm
from requests import get


log = getLogger(__name__)


CHUNK_SIZE = 2**10


def is_url(url):
    """
    Deterime if given string is an url.

    :param str url: String to check if its a URL.
    :return: True if its an URL, False otherwise.
    :rtype: bool
    """
    return urlparse(url).scheme != ''


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

    filename = basename(url)
    name, ext = splitext(filename)
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
        with tqdm(
                total=size, unit='B', unit_scale=True,
                leave=True, desc=filename
                ) as pbar:
            for block in response.iter_content():
                bytes_read = len(block)
                total += bytes_read
                pbar.update(bytes_read)
                fd.write(block)

    log.info(
        'Done. File saved in {} ({:.2f})MBs'.format(
            fd.name, total / 1000000
        )
    )
    return fd.name


def sha256(filename):
    """
    Calculate SHA256 of given filename.

    :param str filename: Filename to calculate SHA256 from.
    :return: SHA256 hexidecimal digest.
    :rtype: str
    """
    sha = sha256lib()

    with open(filename, 'rb') as fd:
        while True:
            block = fd.read(CHUNK_SIZE)
            if not block:
                break
            sha.update(block)

    digest = sha.hexdigest()
    log.info('File {} has a SHA256 digest of {}'.format(filename, digest))
    return digest


def unzip(filename):
    """
    Unzip given filename.

    The extraction folder will be determined by the archive filename removing
    the extension, including it's parent folder.

    :param str filename: Path to the zip to extract.
    :return: The path where the archive was extracted.
    :rtype: str
    """
    def determine_extract_path(member, extract_dir):
        # FIXME: Make this secure and cross-platform
        return join(extract_dir, member.filename)

    filename = abspath(filename)
    extract_dir = splitext(filename)[0]

    with ZipFile(filename, 'r') as zhandler:
        # Test zip file
        if zhandler.testzip():
            raise Exception('Zip file {} is corrupt.'.format(filename))

        # Ensure extraction directory now that we know the archive is valid
        ensure_dir(extract_dir)

        # Determine file uncompressed size
        members = zhandler.infolist()
        size = sum(m.file_size for m in members)

        # Progress bar
        with tqdm(
                total=size, unit='B', unit_scale=True,
                leave=True, desc=basename(filename)) as pbar:

            # Extract each member
            for member in members:

                # Determine extraction path
                extract_path = determine_extract_path(member, extract_dir)

                # Create directory if required
                if member.filename[-1] == '/':
                    ensure_dir(extract_path)
                    continue

                with zhandler.open(member) as compressed, \
                        open(extract_path, 'wb') as uncompressed:

                    while True:
                        block = compressed.read(CHUNK_SIZE)
                        if not block:
                            break
                        bytes_read = len(block)
                        pbar.update(bytes_read)
                        uncompressed.write(block)

    return extract_dir


__all__ = [
    'is_url',
    'ensure_dir',
    'download',
    'sha256',
    'unzip'
]

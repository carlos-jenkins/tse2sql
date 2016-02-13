.. toctree::
   :hidden:

   developer
   tse2sql/tse2sql

======================================
Convertidor del Padron Electoral a SQL
======================================

.. container:: float-right

   .. image:: _static/images/logo.png

Convertidor a SQL del padrón electoral publicado en CSV por el Tribunal Supremo
de Elecciones


Install
=======

You require the Python packages installer ``pip``, see:

    https://pip.pypa.io/en/stable/installing/

Then, install the ``tse2sql`` package:

.. code-block:: bash

    sudo pip install tse2sql


Usage
=====

.. code-block:: text

    $ pip3 install tse2sql
    $ tse2sql --help
    usage: tse2sql [-h] [-v] [--version] [--renderer {mysql}] [archive]

    Convertidor a SQL del padrón electoral publicado en CSV por el Tribunal
    Supremo de Elecciones

    positional arguments:
      archive               URL or path to the voters database

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase verbosity level
      --version             show program's version number and exit
      --renderer {mysql}  SQL renderer to use


Where ``archive`` can be left empty and the known URL where the voters database
is published will be used. A local path to a ``.zip`` file can also be used
to avoid download of the database if it is already in the local system.

When run, ``tse2sql`` will create a few files in the current working directory:

:``<digest>.data.sjon``: Analysis of the ``Distelec.txt`` data. This JSON file
 provides a dictionary the amount of provinces, cantons and districts,
 the largest name of those, and the bad lines found.
:``<digest>.<renderer>.sql``: The SQL version of the database.

The whole process, downloading, extracting, parsing and writing the output
will take several minutes to finish. ``tse2sql`` was optimized for memory
usage, so expect high CPU usage while writing the outputs.


MySQL
+++++

You will need a functional MySQL server install, see:

    https://www.linode.com/docs/databases/mysql/how-to-install-mysql-on-ubuntu-14-04

Load the database and create a user for it:

.. code-block:: text

    $ mysql -u root -p
    mysql> SET @start := NOW(); source <DIGEST>.mysql.sql; SET @end := NOW(); SELECT TIMEDIFF(@end, @start);
    mysql> GRANT ALL PRIVILEGES ON tse2sql.* TO 'tse2sql'@'localhost' IDENTIFIED BY '<YOUR_PASSWORD>';

Sourcing the database will take several minutes. Once done you will most likely
use the following query:

.. code-block:: mysql

    SELECT * FROM voter
        JOIN district ON voter.district_id_district = district.id_district
        JOIN canton ON district.canton_id_canton = canton.id_canton
        JOIN province ON canton.province_id_province = province.id_province
        WHERE voter.id_voter = <id_voter>;


Contributing
============

- :doc:`Developer Guide. <developer>`
- :doc:`Internal Documentation Reference. <tse2sql/tse2sql>`
- `Project repository. <https://github.com/carlos-jenkins/tse2sql>`_


License
=======

::

   Copyright (C) 2016 Carlos Jenkins

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

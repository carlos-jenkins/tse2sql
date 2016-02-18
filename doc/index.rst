.. toctree::
   :hidden:

   developer
   tse2sql/tse2sql

======================================
Convertidor del Padron Electoral a SQL
======================================

.. container:: float-right

   .. image:: _static/images/logo.png

SQL converter of the electoral registry published by the Costa Rican Supreme
Electoral Tribunal.

.. contents:: Table of Contents
   :local:


Install
=======

You require the Python packages installer for Python 3 ``pip3``, see:

    https://pip.pypa.io/en/stable/installing/

Then, install the ``tse2sql`` package:

.. code-block:: bash

    sudo pip3 install tse2sql


Converter Usage
===============

.. code-block:: text

    $ pip3 install tse2sql
    $ tse2sql --help
    usage: tse2sql [-h] [-v] [--version] [--renderer {mysql}] [archive]

    SQL converter of the electoral registry published by the Costa Rican
    Supreme Electoral Tribunal.

    positional arguments:
      archive               URL or path to the voters database

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase verbosity level
      --version             show program's version number and exit
      --renderer {mysql}  SQL renderer to use


Where ``archive`` can be left empty and the known URL where the voters database
is published will be used, currently:

::

    http://www.tse.go.cr/zip/padron/padron_completo.zip

A local path to a ``.zip`` file can also be used to avoid download of the
database if it is already in the local system.

When run, ``tse2sql`` will create a few files in the current working directory:

:``<digest>.<renderer>.sql``: The SQL version of the database.
:``<digest>.data.json``: Analysis of the ``Distelec.txt`` data. This JSON file
 provides a dictionary with the amount of provinces, cantons and districts,
 the largest name of those, and the bad lines found.
:``<digest>.samples.json``: A fil with samples of voters ids for each
 district. This is the input file for the scrapper.

The whole process, downloading, extracting, parsing and writing the output
will take several minutes to finish. ``tse2sql`` was optimized for memory
usage, so expect high CPU usage while writing the outputs.


Scrapper Usage
==============

.. code-block:: text

    tse2sql-scrapper --help
    usage: tse2sql-scrapper [-h] [-v] [--version] [--renderer {mysql}] samples

    TSE Voting Sites Scrapper

    positional arguments:
      samples             Samples file with one id number per site id

    optional arguments:
      -h, --help          show this help message and exit
      -v, --verbose       Increase verbosity level
      --version           show program's version number and exit
      --renderer {mysql}  SQL renderer to use


Some data isn't published in CSV by the Supreme Electoral Tribunal:

#. Voting center names. There is one voting center per district AFAWK.
#. Voting centers addresses.
#. Geographical coordinates of the voting center.

Currently there is a web service available at:

.. code-block:: text

    http://www.tse.go.cr/DondeVotarM/prRemoto.aspx/ObtenerDondeVotar

That allows to grab this information as following:

.. code-block:: text

    curl -i -X POST -H "Content-Type: application/json" -d '{"numeroCedula":"100763791"}' $WEB_SERVICE_ENDPOINT

This request will return the first two data as is and an url to Google Maps.
The ``tse2sql-scrapper`` will parse that URL for the coordinates.


Databases
=========

MySQL
+++++

The schema of the database is as follows:

   .. image:: _static/images/schema_mysql.png

You will need a functional MySQL server install, see:

    https://www.linode.com/docs/databases/mysql/how-to-install-mysql-on-ubuntu-14-04

This database uses ``FULLTEXT INDEX`` on a InnoDB engine, and thus, requires
at least MySQL v5.6. On Ubuntu Linux:

.. code-block:: bash

    sudo apt-get install mysql-server-5.6

Load the database and create a user for it:

.. code-block:: text

    $ mysql -u root -p
    mysql> SET @start := NOW(); source <DIGEST>.mysql.sql; SET @end := NOW(); SELECT TIMEDIFF(@end, @start);
    mysql> SET @start := NOW(); source <DIGEST>.scrapped.mysql.sql; SET @end := NOW(); SELECT TIMEDIFF(@end, @start);
    mysql> GRANT ALL PRIVILEGES ON tsesql.* TO 'tse2sql'@'localhost' IDENTIFIED BY '<YOUR_PASSWORD>';


Sourcing the database will take several minutes. Once done you will most likely
use the following query:

.. code-block:: mysql

    SELECT id_voter, name, family_name_1, family_name_2, sex, id_expiration,
        name_province, name_canton, name_district, site,
        voting_center_name, voting_center_address,
        voting_center_latitude, voting_center_longitude
    FROM voter
        JOIN district ON voter.district_id_district = district.id_district
        JOIN canton ON district.canton_id_canton = canton.id_canton
        JOIN province ON canton.province_id_province = province.id_province
    WHERE voter.id_voter = <id_voter>;


If you don't have the voter id but you have the name you could use the following
query (adding the + sign at the beginning of each word is important to get
matching res):

.. code-block:: mysql

    SELECT id_voter, name, family_name_1, family_name_2, sex, id_expiration,
        name_province, name_canton, name_district, site,
        voting_center_name, voting_center_address,
        voting_center_latitude, voting_center_longitude
    FROM voter
        JOIN district ON voter.district_id_district = district.id_district
        JOIN canton ON district.canton_id_canton = canton.id_canton
        JOIN province ON canton.province_id_province = province.id_province
    WHERE MATCH(name, family_name_1, family_name_2)
        AGAINST ('+<name> +<family_name_1> +<family_name_2>' IN BOOLEAN MODE);


To implement the full search, MySQL uses Boolean logic, in which

.. code-block:: text

    + stands for AND
    - stands for NOT
    [no operator] implies OR

The minimum default token size in InnoDB is 3 characters and the indexing
engine ignores words shorter than this minimum size, then when the length of
the token is minor than 3 no operator should be added to get more accurate
results.


REST APIs
=========

Under the ``apis`` folder exists two example implementations of a REST API
using this database. One in NodeJS and one in Python-Flask. Both share the
same behavior with two endpoints:

.. code-block:: text

    /voter/info-by-id/<voter_id>
    /voter/info-by-name/<Name of the voter>

Instructions to how to run those REST APIs is available in each subproject
``README.rst`` file.


Android App
===========

You can download the Android App *¿Dónde Voto?* here:

    http://carlos.jenkins.co.cr/software/donde-voto.apk

The project repository for this app is located at:

    https://github.com/caroaguilar/tse-info-app


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

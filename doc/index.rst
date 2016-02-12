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

::

    sudo pip install tse2sql


Usage
=====

::

    $ pip install tse2sql
    $ tse2sql --help
    usage: tse2sql [-h] [-v] [--version] [--template {mysql,sqlite}] [archive]

    Convertidor a SQL del padrón electoral publicado en CSV por el Tribunal
    Supremo de Elecciones

    positional arguments:
      archive               URL or path to the voters database

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase verbosity level
      --version             show program's version number and exit
      --template {mysql,sqlite}
                            SQL template to use


Where ``archive`` can be left empty and the known URL where the voters database
is published will be used. A local path to a ``.zip`` file can also be used
to avoid download of the database if it is already in the local system.

When run, ``tse2sql`` will create a few files in the current working directory:

:``<digest>.data.sjon``: Analysis of the ``Distelec.txt`` data. This JSON file
 provides a dictionary the amount of provinces, cantons and districts,
 the largest name of those, and the bad lines found.
:``<digest>.<template>.sql``: The SQL version of the database.


MySQL
+++++

You will need a functional MySQL server install, see:

    https://www.linode.com/docs/databases/mysql/how-to-install-mysql-on-ubuntu-14-04

Then you need to create the database and user:

::

    $ mysql -u root -p
    mysql> CREATE DATABASE tse2sql;
    mysql> GRANT ALL PRIVILEGES ON tse2sql.* TO 'tse2sql'@'localhost' IDENTIFIED BY 'PUTYOURKEYHERE';

Finally, load the schema and data from the generated file:

::

    mysql -u root -p tse2sql < [DIGEST].mysql.sql


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

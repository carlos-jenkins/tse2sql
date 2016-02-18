=================================
Python-Flask REST API for TSE2SQL
=================================

Very basic example REST API for the tse2sql project.


Usage
=====

.. code-block:: bash

   sudo pip3 install -r requirements.txt
   nano settings.json
   ./app.py


Deploy
======

Apache
++++++

This assumes that the ``tsesql`` database is already available, and a user
``tse2sql`` was configured.

.. code-block:: bash

   sudo apt-get install python-virtualenv python3-pip
   sudo -u www-data bash
   pushd /var/www/
   git clone https://github.com/carlos-jenkins/tse2sql.git
   pushd tse2sql/apis/python-api/
   virtualenv --no-site-packages -p /usr/bin/python3.4 venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   deactivate
   nano settings.json
   exit
   sudo nano /etc/apache2/sites-available/your-site.conf

And add the following directives:

.. code-block:: text

   # Handle tse2sql API
   WSGIDaemonProcess tse2sql python-path=/var/www/tse2sql/apis/python-api/venv/lib/python3.4/site-packages
   WSGIScriptAlias /tse2sql /var/www/tse2sql/apis/python-api/app.py

   <Directory "/var/www/tse2sql/apis/python-api">
       WSGIProcessGroup tse2sql
       WSGIApplicationGroup %{GLOBAL}
       Order deny,allow
       Allow from all
   </Directory>

And then restart apache:

.. code-block:: text

   sudo service apache2 restart

Your API will be available at:

.. code-block:: text

   <your_domain>/tse2sql/voter/info-by-id/<id>
   <your_domain>/tse2sql/voter/info-by-name/<name>


License
=======

::

   Copyright (C) 2016 Carolina Aguilar
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

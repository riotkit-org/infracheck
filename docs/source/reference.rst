Predefined check types reference
================================

Infracheck comes by default with some standard checks, there is a list of them:


http
----

Performs a HTTP call using curl.

Example:

.. code:: json

    {
        "type": "http",
        "input": {
            "url": "http://iwa-ait.org",
            "expect_keyword": "iwa",
            "not_expect_keyword": "Server error"
        }
    }


Parameters:

- url
- expect_keyword
- not_expect_keyword

rkd://
------

Infracheck can execute RiotKit-Do tasks. RKD is a task executor, similar to Makefile or Gradle.
It's essential feature is a possibility to load tasks from PyPI (Python packages).


Using RKD you can write a Python class, version and release it to PyPI with a list of dependencies, and install in any place
with PIP. A packaged task can require extra dependencies you do not want always to install eg. MySQL, PostgreSQL, Redis or other clients
you want to selectively install on your Infracheck instances.

More information on how to write RKD tasks: `in RiotKit-Do's documentation <https://riotkit-do.readthedocs.io/en/latest/usage/developing-tasks.html#option-2-for-python-developers-task-as-a-class>`_


.. code:: json

    {
        "type": "rkd://rkd.standardlib.shell:sh",
        "input": {
            "-c": "ps aux |grep X11"
        }
    }


.. code:: json

    {
        "type": "rkd://my_rkd_check:mysql:temporary-table-size-check",
        "input": {
            "--max": "100000",
            "--host: "localhost",
            "--port": 3306,
            "--user": "infracheck",
            "--password": "${TEMP_TABLE_SIZE_CHECK_PASSWORD}"
        }
    }

dir-present
-----------

Checks whenever a directory exists.

Parameters:

- dir

file-present
------------

Checks if file is present.

Parameters:

- file_path

docker-health
-------------

Checks if containers are healthy.

Parameters:

- docker_env_name (it's a prefix, to check only containers that names begins with this - idea of docker-compose)

port-open
---------

Checks if the port is open.

Parameters:

- po_host
- po_port (in seconds)
- po_timeout (in seconds)

replication-running
-------------------

Checks if the MySQL replication is in good state. Works with Docker only.

Parameters:

- container
- mysql_root_password

.. include:: ../../infracheck/checks/free-ram
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/domain-expiration
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/disk-space
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/ovh-expiration
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/ssh-fingerprint
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/ssh-files-checksum
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/ssh-command
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/reminder
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/load-average-auto
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/load-average
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/swap-usage-max-percent
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/influxdb-query
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/postgres
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/postgres-primary-streaming-status
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/postgres-replica-status
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/docker-container-log
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/smtp_credentials_check.py
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/tls
   :start-after: <sphinx>
   :end-before: </sphinx>

.. include:: ../../infracheck/checks/tls-docker-network
   :start-after: <sphinx>
   :end-before: </sphinx>

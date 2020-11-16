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

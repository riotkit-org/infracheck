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

docker-bahub
------------

Monitors RiotKit's File Repository "Bahub" API client for errors.

Parameters:

- container

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

disk-space
----------

Monitors disk space.

Parameters:

- min_req_space (in gigabytes)
- dir (path)

free-ram
--------

Monitors RAM memory usage to notify that a maximum percent of memory was used.

Parameters:

- max_ram_percentage (in percents eg. 80)

domain-expiration
-----------------

Check if the domain is close to expiration date or if it is already expired.

**Notice: Multiple usage of this check can cause a "request limit exceeded" error to happen**

*Suggestion: If you check multiple domains, then separate domains checking from regular health checks and set CHECK_INTERVAL (docker) to once a day, and WAIT_TIME=300 for non-docker installations - in crontab set a check with --force once a day*

Parameters:

- domain (domain name)
- alert_days_before (number of days before expiration date to start alerting)

replication-running
-------------------

Checks if the MySQL replication is in good state. Works with Docker only.

Parameters:

- container
- mysql_root_password

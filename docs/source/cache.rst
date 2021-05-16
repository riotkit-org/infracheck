Cache and freshness
===================

It can be harmful to the server to run all checks on each HTTP endpoint call, so the application is running them periodically every X seconds specified by **--refresh-time** switch or **REFRESH_TIME** environment variable (in docker)

Refresh time
------------

If you use an official docker image, then you can set an environment variable.

Example: check once a day (good for domains whois check).

.. code:: bash

    REFRESH_TIME=86400

From CLI you can set **--refresh-time=86400**

Wait time
---------

Some checks could call external APIs, those can have limits. A good example is a *domain-expiration* check which is using whois.
Set **--wait=60** to for example wait 60 seconds before each check - where check is a single entry on the list of checks.

Customizing check freshness time per check
------------------------------------------

Beside the global setting of **refresh time** there could be a per-check setting called "results_cache_time".

**Example of caching the check result for at least 300 seconds**

.. code:: json

    {
        "type": "swap-usage-max-percent",
        "results_cache_time": "300",
        "input": {
            "max_allowed_percentage": 0
        }
    }

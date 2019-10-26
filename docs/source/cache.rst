Cache and freshness
===================

It can be harmful to the server to run all checks on each HTTP endpoint call, so a cronjob in background is writing results, and HTTP endpoint is reading.

How often really the checks are performing depends on your configuration, how often you execute **infracheck --force**

--force
-------

The *--force* parameter means that the application will write checks results to a cache.

When this flag is not specified, then application will read the data from the cache.

Docker
------

If you use an official docker image, then you can set CHECK_INTERVAL to a crontab-like syntax interval eg. **CHECK_INTERVAL=00 23 * * *** to check once a day (good for domains whois check).

Limits
------

Some checks could call external APIs, those can have limits. A good example is a *domain-expiration* check which is using whois.
It is recommended to run a separate infracheck instance with less frequent checking, eg. once a day - see CHECK_INTERVAL in docker, and crontab in standalone installation.

You can also use `--wait` switch to set waiting in seconds between single checks (in docker it is `WAIT_TIME` variable)

--lazy
------

When running a ex. HTTP endpoint without `--force`, then application is only reading results of previously executed checks that are usually executed in background using cron.
**Without lazy** the checks that were not executed yet will be showing "Not ready yet" and a **status equals to false**.
If you really need to avoid such case, **then you can allow running a check on-demand by enabling** `--lazy` **flag** (LAZY=true in docker).

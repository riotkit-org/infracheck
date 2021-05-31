Check configuration reference
#############################

.. code:: json

    {
        "type": "http",
        "description": "IWA-AIT check",
        "results_cache_time": 300,
        "input": {
            "url": "http://iwa-ait.org",
            "expect_keyword": "iwa",
            "not_expect_keyword": "Server error"
        },
        "hooks": {
            "on_each_up": [
                "rm -f /var/www/maintenance.html"
            ],
            "on_each_down": [
                "echo \"Site under maintenance\" > /var/www/maintenance.html"
            ]
        },
        "quiet_periods": [
            {"starts": "30 00 * * *", "duration": 60}
        ]
    }


type
****

Name of the binary/script file placed in the "checks" directory. At first will look at path specified by "--directory"
CLI parameter, then will fallback to Infracheck internal check library.

Example values:

- disk-space
- load-average
- http
- smtp_credentials_check.py


description
***********

Optional text field, there can be left a note for other administrators to exchange knowledge in a quick way in case
of a failure.


results_cache_time
******************

How long the check result should be kept in cache (in seconds)


input
*****

Parameters passed to the binary/script file (chosen in "type" field). Case insensitive, everything is converted
to UPPERCASE and passed as environment variables.

**Notice:** *Environment variables and internal variables can be injected using templating feature - check* :ref:`Templating`

hooks
*****

(Optional) Execute shell commands on given events.

- on_each_up: Everytime the check is OK
- on_each_down: Everytime the check is FAILING


quiet_periods
*************

(Optional) Defines time, when the check results should be ignored. For example setting "30 00 * * *" and 60m duration will
result in ignoring check failure at 00:30 everyday for 60 minutes - till 01:30

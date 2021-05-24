Check configuration reference
#############################

.. code:: json

    {
        "type": "http",
        "description": "IWA-AIT check",
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
        }
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


input
*****

Parameters passed to the binary/script file (chosen in "type" field). Case insensitive, everything is converted
to UPPERCASE and passed as environment variables.

**Notice:** *Environment variables and internal variables can be injected using templating feature - check* :ref:`Templating`

hooks
*****

Execute shell commands on given events.

- on_each_up: Everytime the check is OK
- on_each_down: Everytime the check is FAILING


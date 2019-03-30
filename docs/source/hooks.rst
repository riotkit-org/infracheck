Hooks
=====

After each execution of your checks there is a possibility to execute some commands.

**Example:**

.. code:: json

    {
        "type": "disk-space",
        "input": {
            "dir": "/",
            "min_req_space": "6"
        },
        "hooks": {
            "on_each_up": [
                "rm -f /tmp/maintenance.html"
            ],
            "on_each_down": [
                "echo \"Site under maintenance\" > /tmp/maintenance.html"
            ]
        }
    }

Example above will delete a */tmp/maintenance.html* file when disk space will be at acceptable level.
If there will be no enough disk space, then "Site under maintenance" will be written to the /tmp/maintenance.html
With this practical example you can add a rule to your NGINX/Apache gateway to show a maintenance page, when a file is present.

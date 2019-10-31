.. _Templating:

Templating
==========

In order to increase the security there is a `simple templating` mechanism that allows to inject variables into
parameters you define that are passed to the checks.

**Example:**

.. code:: yaml

    {
        "type": "ssh-command",
        "input": {
            "user": "thesecurityman",
            "host": "iwa-ait.org",
            "port": 6200,
            "password": "${ENV.IWA_SECURITY_MAN_PASSWD}",
            "command": "/usr/bin/some-security-check --is-secure",
            "expected_exit_code": 0,
            "timeout": 30
        }
    }

Reference table
---------------

+--------------+------------------------------+--------------------------------------------------+
| Pattern      | Example                      | Description                                      |
+==============+==============================+==================================================+
| ${ENV.*}     | ${ENV.USER}                  | Injects an environment variable from the host    |
+--------------+------------------------------+--------------------------------------------------+
| ${checkName} | http                         | Name of the currently executed check             |
+--------------+------------------------------+--------------------------------------------------+
| ${date}      | 2019-10-31T07:53:45.380307   | Current date and time                            |
+--------------+------------------------------+--------------------------------------------------+

Example strategy of deploying passwords with Docker Compose and Ansible
-----------------------------------------------------------------------

1. Encrypt your passwords with ansible-vault
2. Decrypt them during deployment into `.env` on target machine for docker-compose
3. In docker-compose service definition pass variable explicitly from the `.env` file

.. code:: yaml

    environment:
        # variables in checks
        - IWA_SECURITY_MAN_PASSWD=${IWA_SECURITY_MAN_PASSWD}

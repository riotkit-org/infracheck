Quick start
===========

To monitor applications and the infrastructure parts you need to configure **checks**.
A configured check is a json file that defines a method name (script to be used) and the input parameters.
Each check is executed when your external monitoring software invokes the HTTP endpoint, or when you execute the shell command.


Infracheck can work as a HTTP endpoint responding with JSON, or as a console command.

.. image:: _static/quick-start.png
   :target: https://asciinema.org/a/237795

1. Structure
------------

You need to create a **project structure** from following template:

.. code:: yaml

    - checks/
        - http
        - smtp
        - port
    - configured/
        - redis
        - duckduckgo_http
        - smtp_is_alive

In **checks** there should be scripts that will take parameters as environment variables, process and give results.
For simpler cases you may not need to define any scripts, just configure pre-defined ones.


**configured** should contain your actual use cases, for example "duckduckgo_http" from above example could use "http" check with url "https://duckduckgo.com" as a parameter.

2. Configuring a first check
----------------------------

Let's assume that we need to check if a page contains given keyword, and does not contain another defined one.
Following check will use **curl** to fetch page content.

Test cases:

- If page will not load, then THE CHECK RETURNS FAILURE
- If page contains "Server error", then THE CHECK RETURNS FAILURE
- If page will not contain keyword "iwa", then THE CHECK RETURNS FAILURE
- If page loads properly and contains "iwa" keyword, then THE CHECK RETURNS SUCCESS

.. code:: json

    {
        "type": "http",
        "input": {
            "url": "http://iwa-ait.org",
            "expect_keyword": "iwa",
            "not_expect_keyword": "Server error"
        }
    }

3. Running checks
-----------------

**With Docker**

You can use a ready-to-use docker image **wolnosciowiec/infracheck** or **wolnosciowiec/infracheck:armhf** for 32 bit ARM.
The image will by default expose a HTTP endpoint.

.. code:: bash

    sudo docker run --name infracheck -p 8000:8000 -v $(pwd):/data -d --rm wolnosciowiec/infracheck

    # now test it
    curl http://localhost:8000

List of supported environment variables:

- CHECK_INTERVAL="*/1 * * * *"
- WAIT_TIME=0
- LAZY=false

**Without Docker**

.. code:: bash

    git clone https://github.com/riotkit-org/infracheck
    cd infracheck
    make install

    # run checks in the shell
    infracheck --directory=/your-project-directory-path-there

    # run a webserver
    infracheck --directory=/your-project-directory-path-there --server --server-port=7422 --lazy

    # set up a scheduled checking
    echo "*/1 * * * * infracheck --directory=/your-project-directory-path-there --force" >> /etc/crontabs/root

**Using PIP**

.. code:: bash

    sudo pip install infracheck

    # run checks in the shell
    infracheck --directory=/your-project-directory-path-there

    # run a webserver
    infracheck --directory=/your-project-directory-path-there --server --server-port=7422

    # set up a scheduled checking
    echo "*/1 * * * * infracheck --directory=/your-project-directory-path-there --force" >> /etc/crontabs/root


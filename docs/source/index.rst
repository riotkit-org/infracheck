
RiotKit's Infracheck
====================

HTTP healthcheck endpoint + shell healthcheck runner.
Simple, easy to setup, easy to understand. Works perfectly with Docker. A perfectly fitting universal brick in your monitoring.

.. code:: json

   {
       "checks": {
           "disk-space": {
               "ident": "disk-space=True",
               "output": "There is 350.8GB disk space at '/', nothing to worry about, defined minimum is 15GB\n",
               "status": true
           },
           "docker-health": {
               "ident": "docker-health=True",
               "output": "Docker daemon reports that there is no 'unhealthy' service running in '' space\n",
               "status": true
           },
           "minio": {
               "ident": "minio=True",
               "output": "",
               "status": true
           },
           "replication-running": {
               "ident": "replication-running=True",
               "output": "Replica seems to be in good state\n",
               "status": true
           },
           "storage-synchronization": {
               "ident": "storage-synchronization=True",
               "output": "Storage synchronization looks fine\n",
               "status": true
           }
       },
       "global_status": true
   }


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   first-steps
   hooks
   reference
   templating
   custom-scripts
   cache

From authors
============

Project was started as a part of RiotKit initiative, for the needs of grassroot organizations such as:

- Fighting for better working conditions syndicalist (International Workers Association for example)
- Tenants rights organizations
- Various grassroot organizations that are helping people to organize themselves without authority

.. rst-class:: language-en align-center

*RiotKit Collective*

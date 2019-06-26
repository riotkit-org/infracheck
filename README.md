InfraCheck
==========

[![Documentation Status](https://readthedocs.org/projects/infracheck/badge/?version=latest)](https://infracheck.docs.riotkit.org/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/riotkit-org/infracheck.svg?branch=master)](https://travis-ci.org/riotkit-org/infracheck)
![Docker Build Status](https://img.shields.io/docker/build/wolnosciowiec/infracheck.svg)
![GitHub release](https://img.shields.io/github/release/riotkit-org/infracheck.svg?style=popout)
![PyPI](https://img.shields.io/pypi/v/infracheck.svg?style=popout)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/infracheck.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/infracheck.svg)
[![codecov](https://codecov.io/gh/riotkit-org/infracheck/branch/master/graph/badge.svg)](https://codecov.io/gh/riotkit-org/infracheck)

Health check system designed to be easy to extend by not enforcing the programming language.
A single health check unit (let we call it later just 'check') can be written even in BASH.

Read more in the documentation at: https://infracheck.docs.riotkit.org/en/latest/

Dictionary
----------

- `script` - a script that is checking something
- `check` - your definition (input arguments) how to use a `check` eg. "type": http + params what is the URL, you can define multiple configurations for single check


Guide to "check" creation
-------------------------
1. Write a `script` in any programming language, take environment variables as input (skip this step if you want to use existing pre-defined scripts)
2. Create a json `check` that will contain a working configuration example for your `script`.

Running
-------

See a working example in the `./example` directory.

```bash
# from this directory
make install

infracheck --help
```

docker or docker-compose:

```yaml
version: '2'
services:
    healthcheck:
        image: wolnosciowiec/infracheck
        command: " --directory=/data --server-path-prefix=/some-prefix"
        volumes:
            # place your health checks structure at ./healthchecks
            - "./healthchecks:/data"
            - "/var/run/docker.sock:/var/run/docker.sock:ro"
        ports:
            - "8000:8000"
        #labels:
        #    - "traefik.frontend.rule=Host: health.localhost; PathPrefix: /some-prefix"
        #    - "traefik.enable=true"
        #    - "traefik.basic.protocol=${PROTO}"
        #    - "traefik.port=8000"
```

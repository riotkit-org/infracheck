InfraCheck
==========

Health check system designed to be easy to extend by not enforcing the programming language.
A single health check unit (let we call it later just 'check') can be written even in BASH.


Dictionary
----------

- `check` - a script that is checking something
- `configuration` - your definition how to use a `check` eg. "type": http + params what is the URL, you can define multiple configurations for single check
- `template` - working example of `configuration`


How it works?
-------------
1. Write a `check` in any programming language, take environment variables as input.
2. Create a json `template` that will contain a working configuration example for your `check`.
3. You can skip 1 and 2 if you want to use already created checks
4. Create a `configuration` to use a `check` in *specified context

Running
-------

See a working example in the `./example` directory.

```bash
# from this directory
python ./infracheck/bin.py --help
```

Docker-compose:

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

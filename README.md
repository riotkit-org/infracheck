InfraCheck
==========

[![Documentation Status](https://readthedocs.org/projects/infracheck/badge/?version=latest)](https://infracheck.docs.riotkit.org/en/latest/?badge=latest)
![Test and release a package](https://github.com/riotkit-org/infracheck/workflows/Test%20and%20release%20a%20package/badge.svg)
![GitHub release](https://img.shields.io/github/release/riotkit-org/infracheck.svg?style=popout)
![PyPI](https://img.shields.io/pypi/v/infracheck.svg?style=popout)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/infracheck.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/infracheck.svg)
[![codecov](https://codecov.io/gh/riotkit-org/infracheck/branch/master/graph/badge.svg)](https://codecov.io/gh/riotkit-org/infracheck)

Health check system designed to be easy to extend by not enforcing the programming language.
A single health check unit (let we call it later just 'check') can be written even in BASH.

Read more in the documentation at: https://infracheck.docs.riotkit.org/en/latest/


Running with Docker Compose
---------------------------

See a working example in the `./example` directory.

Standalone installation and running
-----------------------------------

From sources:

```bash
# from this directory
rkd :install

infracheck --help
```

From PIP:

```bash
pip install infracheck

infracheck --help
```

External dependencies
---------------------

- **whois** commandline tool (`apt-get install whois`)
- **sshpass** (`apt-get install sshpass`)
- **openssl**

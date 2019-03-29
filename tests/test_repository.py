import unittest
import sys
import os
import inspect
from unittest_data_provider import data_provider

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../app'
sys.path.append(path)
from infracheck.repository import Repository

# for static analysis
if False:
    from ..app.infracheck.repository import Repository


class RepositoryTest(unittest.TestCase):

    def test_returns_all_checks(self):
        repository = Repository([path + '/../example/healthchecks', path])

        self.assertEqual(
            sorted(['is_dd_accessible', 'docker-health', 'some_port_is_open', 'disk-space', 'hello-test-custom-check-example']),
            sorted(repository.get_configured_checks(with_disabled=False))
        )

        self.assertIn('some-disabled', repository.get_configured_checks(with_disabled=True))

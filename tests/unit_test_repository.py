import unittest
import sys
import os
import inspect

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.repository import Repository


class RepositoryTest(unittest.TestCase):

    def test_returns_all_checks(self):
        repository = Repository([path + '/example/healthchecks', path], '/tmp/.infracheck.sqlite3')

        self.assertEqual(
            sorted([
                'is_dd_accessible', 'docker-health', 'domain-expiration', 'some_port_is_open',
                'disk-space', 'hello-test-custom-check-example', 'ram', 'rkd-sh']),
            sorted(repository.get_configured_checks(with_disabled=False))
        )

        self.assertIn('some-disabled', repository.get_configured_checks(with_disabled=True))

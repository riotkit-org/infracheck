import unittest
import docker
import os

from tempfile import NamedTemporaryFile
from tests.utils import run_check
from tests.utils.ssh_test import SSHServerContainerRequirement


class SshCommandCheckTest(SSHServerContainerRequirement, unittest.TestCase):
    docker_client: docker.DockerClient

    def test_fingerprint_will_be_fetched_first_time(self):
        known_hosts_file = NamedTemporaryFile(delete=False)

        result = run_check('ssh-command', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'USER': 'root',
            'PASSWORD': 'root',
            'KNOWN_HOSTS_FILE': known_hosts_file.name,
            'SSH_OPTS': '',  # there is no StrictHostKeyChecking turned off
            'COMMAND': 'ls -la'
        }, {})

        os.unlink(known_hosts_file.name)

        self.assertEqual('OK', result.output.strip())
        self.assertTrue(result.exit_status)

    def test_not_passed_host_raises_human_readable_message(self):
        result = run_check('ssh-command', {}, {})

        self.assertIn('HOST is mandatory', result.output.strip())
        self.assertFalse(result.exit_status)

    def test_success_case(self):
        """
        Simple success case with expected keywords usage
        :return:
        """

        result = run_check('ssh-command', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'USER': 'root',
            'PASSWORD': 'root',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
            'COMMAND': 'uname -a',
            'EXPECTED_KEYWORDS': 'Linux',
            'UNEXPECTED_KEYWORDS': 'Darwin'
        }, {})

        self.assertEqual('OK', result.output.strip())
        self.assertTrue(result.exit_status)

    def test_invalid_password(self):
        result = run_check('ssh-command', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'USER': 'root',
            'PASSWORD': 'invalid-password',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
        }, {})

        self.assertIn('Permission denied, please try again.', result.output.strip())
        self.assertFalse(result.exit_status)

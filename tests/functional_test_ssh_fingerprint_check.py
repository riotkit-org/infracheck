import unittest
import docker

from tests.utils import run_check
from tests.utils.ssh_test import SSHServerContainerRequirement


class SshFingerprintTest(SSHServerContainerRequirement, unittest.TestCase):
    docker_client: docker.DockerClient

    def test_success_case(self):
        # we create SSH server for testing dynamically in a docker container, so each time it has a different identity
        current_expected_fingerprint = self.get_current_ssh_server_fingerprint()

        result = run_check('ssh-fingerprint', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'EXPECTED_FINGERPRINT': current_expected_fingerprint
        }, {})

        self.assertEqual('Fingerprint is OK', result.output.strip())
        self.assertTrue(result.exit_status)

    def test_invalid_fingerprint(self):
        result = run_check('ssh-fingerprint', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'EXPECTED_FINGERPRINT': 'SOME FINGERPRINT THAT DOES NOT MATCH SERVER FINGERPRINT'
        }, {})

        self.assertIn('Fingerprint does not match', result.output.strip())
        self.assertFalse(result.exit_status)

    def test_missing_host_parameter(self):
        result = run_check('ssh-fingerprint', {
            'PORT': 3223,
            'EXPECTED_FINGERPRINT': 'SOME FINGERPRINT THAT DOES NOT MATCH SERVER FINGERPRINT'
        }, {})

        self.assertIn('You need to provide a HOST', result.output.strip())
        self.assertFalse(result.exit_status)

    def test_reports_stderr_messages(self):
        result = run_check('ssh-fingerprint', {
            'HOST': 'non-existing-host',
            'PORT': 3223,
            'EXPECTED_FINGERPRINT': 'BAKUNIN'
        }, {})

        self.assertIn('getaddrinfo non-existing-host', result.output.strip())
        self.assertFalse(result.exit_status)

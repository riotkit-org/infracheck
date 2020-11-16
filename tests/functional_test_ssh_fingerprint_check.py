import unittest
import docker

from tests.utils import run_check
from tests.utils.ssh_test import SSHServerContainerRequirement


class SshFingerprintTest(SSHServerContainerRequirement, unittest.TestCase):
    docker_client: docker.DockerClient

    def test_success_case(self):
        stdout: str
        result: int

        # we create SSH server for testing dynamically in a docker container, so each time it has a different identity
        current_expected_fingerprint = self.get_current_ssh_server_fingerprint()

        stdout, result, hooks_output = run_check('ssh-fingerprint', {
            'HOST': 'localhost',
            'PORT': 3222,
            'EXPECTED_FINGERPRINT': current_expected_fingerprint
        }, {})

        self.assertEqual('Fingerprint is OK', stdout.strip())
        self.assertTrue(result)

    def test_invalid_fingerprint(self):
        stdout: str
        result: int

        stdout, result, hooks_output = run_check('ssh-fingerprint', {
            'HOST': 'localhost',
            'PORT': 3222,
            'EXPECTED_FINGERPRINT': 'SOME FINGERPRINT THAT DOES NOT MATCH SERVER FINGERPRINT'
        }, {})

        self.assertIn('Fingerprint does not match', stdout.strip())
        self.assertFalse(result)

    def test_missing_host_parameter(self):
        stdout: str
        result: int

        stdout, result, hooks_output = run_check('ssh-fingerprint', {
            'PORT': 3222,
            'EXPECTED_FINGERPRINT': 'SOME FINGERPRINT THAT DOES NOT MATCH SERVER FINGERPRINT'
        }, {})

        self.assertIn('You need to provide a HOST', stdout.strip())
        self.assertFalse(result)

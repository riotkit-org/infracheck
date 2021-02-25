import unittest
import docker

from tests.utils import run_check
from tests.utils.ssh_test import SSHServerContainerRequirement


class SshCommandCheckTest(SSHServerContainerRequirement, unittest.TestCase):
    docker_client: docker.DockerClient

    def test_not_passed_host_raises_human_readable_message(self):
        result = run_check('ssh-files-checksum', {}, {})

        self.assertIn('HOST is mandatory', result.output.strip())
        self.assertFalse(result.exit_status)

    def test_success_case(self):
        result = run_check('ssh-files-checksum', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'USER': 'root',
            'PASSWORD': 'root',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
            'EXPECTS': {
                "/dev/null": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        }, {})

        self.assertEqual('All checksums are matching', result.output.strip())
        self.assertTrue(result.exit_status)

    def test_at_least_one_checksum_not_matching(self):
        result = run_check('ssh-files-checksum', {
            'HOST': '127.0.0.1',
            'PORT': 3223,
            'USER': 'root',
            'PASSWORD': 'root',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
            'EXPECTS': {
                "/dev/null": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "/bin/sh": "will-not-match-this-one"
            }
        }, {})

        self.assertIn("FAIL: '/bin/sh' checksum is not matching. Expected: 'will-not-match-this-one'", result.output.strip())
        self.assertFalse(result.exit_status)

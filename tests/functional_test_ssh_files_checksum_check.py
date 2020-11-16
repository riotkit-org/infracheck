import unittest
import docker

from tests.utils import run_check
from tests.utils.ssh_test import SSHServerContainerRequirement


class SshCommandCheckTest(SSHServerContainerRequirement, unittest.TestCase):
    docker_client: docker.DockerClient

    def test_not_passed_host_raises_human_readable_message(self):
        stdout: str
        result: int

        stdout, result, hooks_output = run_check('ssh-files-checksum', {}, {})

        self.assertIn('HOST is mandatory', stdout)
        self.assertFalse(result)

    def test_success_case(self):
        stdout: str
        result: int

        stdout, result, hooks_output = run_check('ssh-files-checksum', {
            'HOST': 'localhost',
            'PORT': 3222,
            'USER': 'root',
            'PASSWORD': 'root',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
            'EXPECTS': {
                "/dev/null": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        }, {})

        self.assertEqual('All checksums are matching', stdout.strip())
        self.assertTrue(result)

    def test_at_least_one_checksum_not_matching(self):
        stdout: str
        result: int

        stdout, result, hooks_output = run_check('ssh-files-checksum', {
            'HOST': 'localhost',
            'PORT': 3222,
            'USER': 'root',
            'PASSWORD': 'root',
            'SSH_OPTS': '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null',
            'EXPECTS': {
                "/dev/null": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "/bin/sh": "will-not-match-this-one"
            }
        }, {})

        self.assertIn("FAIL: '/bin/sh' checksum is not matching. Expected: 'will-not-match-this-one'", stdout.strip())
        self.assertFalse(result)

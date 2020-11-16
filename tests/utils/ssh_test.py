
import subprocess
import time
from .base_docker_container_test import BaseDockerContainerRequirement


class SSHServerContainerRequirement(BaseDockerContainerRequirement):
    @staticmethod
    def _wait_for_container_to_be_ready():
        out = ''

        for i in range(1, 600):
            try:
                out += str(subprocess.check_output('echo "ttttt\n\n" | nc -w 1 "localhost" "3222"',
                                                   shell=True, stderr=subprocess.STDOUT))

                if "SSH-2.0-OpenSSH" in out:
                    return
            except subprocess.CalledProcessError:
                time.sleep(0.5)

        raise Exception('SSH container did not get up properly. Output: ' + out)

    @staticmethod
    def get_current_ssh_server_fingerprint():
        return subprocess.check_output(
            'ssh-keyscan -t rsa -p 3222 localhost', stderr=subprocess.DEVNULL, shell=True
        ).decode('utf-8')

    @staticmethod
    def _get_container_name() -> str:
        return 'ssh'

    @staticmethod
    def _get_ports() -> dict:
        return {'22/tcp': 3222}

    @staticmethod
    def _get_image_name() -> str:
        return 'sickp/alpine-sshd:7.5'

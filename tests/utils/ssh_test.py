
import subprocess
import time
from .base_docker_container_test import BaseDockerContainerRequirement


class SSHServerContainerRequirement(BaseDockerContainerRequirement):
    @staticmethod
    def _wait_for_container_to_be_ready():
        out = ''

        print('Spawning SSH container')

        for i in range(1, 600):
            try:
                out += str(subprocess.check_output('echo "ttttt\n\n" | nc -w 1 "127.0.0.1" "3223"',
                                                   shell=True, stderr=subprocess.STDOUT))

                if "SSH-2.0-OpenSSH" in out:
                    print('SSH container is ready')
                    time.sleep(1)
                    return

            except subprocess.CalledProcessError:
                time.sleep(0.5)

        raise Exception('SSH container did not get up properly. Output: ' + out)

    @staticmethod
    def get_current_ssh_server_fingerprint():
        try:
            return subprocess.check_output(
                'ssh-keyscan -t rsa -p 3223 127.0.0.1', stderr=subprocess.PIPE, shell=True
            ).decode('utf-8')
        except subprocess.CalledProcessError as err:
            return err.stderr.decode('utf-8') + "\n" + err.stdout.decode('utf-8')

    @staticmethod
    def _get_container_name() -> str:
        return 'ssh'

    @staticmethod
    def _get_ports() -> dict:
        return {'22/tcp': 3223}

    @staticmethod
    def _get_image_name() -> str:
        return 'sickp/alpine-sshd:7.5'

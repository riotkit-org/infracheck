
import docker
import docker.errors
import subprocess
import time


class TestThatRequiresSshServer:
    docker_client: docker.DockerClient

    def setUp(self) -> None:
        self.docker_client = docker.from_env()
        self._remove_ssh_container()
        self.docker_client.containers.run('sickp/alpine-sshd:7.5', name='ssh', ports={'22/tcp': 3222}, detach=True)
        self._wait_for_ssh_to_be_ready()

    def tearDown(self) -> None:
        self._remove_ssh_container()

    def _remove_ssh_container(self):
        try:
            container = self.docker_client.containers.get('ssh')

            try:
                container.kill()
            except docker.errors.APIError:
                pass

            container.remove()

        except docker.errors.NotFound:
            pass

    @staticmethod
    def _wait_for_ssh_to_be_ready():
        out = ''

        for i in range(1, 60):
            try:
                out += str(subprocess.check_output('echo "ttttt\n\n" | nc -w 1 "localhost" "3222"',
                                                   shell=True, stderr=subprocess.STDOUT))

                if "SSH-2.0-OpenSSH" in out:
                    return
            except subprocess.CalledProcessError:
                time.sleep(0.5)

        raise Exception('SSH container did not get up properly. Output: ' + out)

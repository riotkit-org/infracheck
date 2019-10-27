
import docker
import docker.errors
import subprocess
import time


class TestThatRequiresSshServer:
    docker_client: docker.DockerClient

    @classmethod
    def setUpClass(cls) -> None:
        TestThatRequiresSshServer.docker_client = docker.from_env()
        TestThatRequiresSshServer._remove_ssh_container()
        TestThatRequiresSshServer.docker_client.containers.run('sickp/alpine-sshd:7.5', name='ssh', ports={'22/tcp': 3222}, detach=True)
        TestThatRequiresSshServer._wait_for_ssh_to_be_ready()

    @classmethod
    def tearDownClass(cls) -> None:
        TestThatRequiresSshServer._remove_ssh_container()
        TestThatRequiresSshServer.docker_client.close()

    @staticmethod
    def _remove_ssh_container():
        try:
            container = TestThatRequiresSshServer.docker_client.containers.get('ssh')

            try:
                container.kill()
            except docker.errors.APIError:
                pass

            container.remove()

        except docker.errors.NotFound:
            pass

    @staticmethod
    def get_current_ssh_server_fingerprint():
        return subprocess.check_output(
            'ssh-keyscan -t rsa -p 3222 localhost', stderr=subprocess.DEVNULL, shell=True
        ).decode('utf-8')

    @staticmethod
    def _wait_for_ssh_to_be_ready():
        out = ''

        for i in range(1, 120):
            try:
                out += str(subprocess.check_output('echo "ttttt\n\n" | nc -w 1 "localhost" "3222"',
                                                   shell=True, stderr=subprocess.STDOUT))

                if "SSH-2.0-OpenSSH" in out:
                    return
            except subprocess.CalledProcessError:
                time.sleep(0.5)

        raise Exception('SSH container did not get up properly. Output: ' + out)


import docker
import docker.errors
import time
from abc import abstractmethod

from docker.models.containers import Container


class BaseDockerContainerRequirement(object):
    docker_client: docker.DockerClient

    @classmethod
    def setUpClass(cls) -> None:
        cls.docker_client = docker.from_env()
        cls._remove_container()
        cls.docker_client.containers.run(cls._get_image_name(), name=cls._get_container_name(), ports=cls._get_ports(),
                                         detach=True, environment=cls._get_environment())
        cls._wait_for_container_to_be_ready()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._remove_container()
        cls.docker_client.close()

    @classmethod
    def _remove_container(cls):
        try:
            container: Container = cls.docker_client.containers.get(cls._get_container_name())

            # try to get logs if container crashed
            try:
                if container.status == 'exited':
                    print('Container "' + cls._get_container_name() + '" crashed, there are logs:', container.logs())
            except:
                pass

            try:
                container.kill()
            except docker.errors.APIError:
                pass

            container.remove()

        except docker.errors.NotFound:
            pass

    @classmethod
    def _wait_for_log_message(cls, message: str, timeout: int = 60):
        container = cls.docker_client.containers.get(cls._get_container_name())

        for sec in range(0, timeout):
            logs = container.logs().decode('utf-8')

            if message in logs:
                return True

            time.sleep(1)

        raise Exception('Message "{message}" not found in container logs'.format(message=message))

    @classmethod
    @abstractmethod
    def _wait_for_container_to_be_ready(cls):
        pass

    @staticmethod
    @abstractmethod
    def _get_container_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def _get_ports() -> dict:
        pass

    @staticmethod
    @abstractmethod
    def _get_image_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def _get_environment() -> dict:
        pass


import docker
import docker.errors
from abc import abstractmethod


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
            container = cls.docker_client.containers.get('ssh')

            try:
                container.kill()
            except docker.errors.APIError:
                pass

            container.remove()

        except docker.errors.NotFound:
            pass

    @staticmethod
    @abstractmethod
    def _wait_for_container_to_be_ready():
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

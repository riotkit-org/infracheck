
import time
from .base_docker_container_test import BaseDockerContainerRequirement

DB = 'test'
USER = 'infracheck'
PASSWORD = 'solidarity_forever'


class InfluxDBContainerRequirement(BaseDockerContainerRequirement):
    @staticmethod
    def _get_environment() -> dict:
        return {
            'INFLUXDB_DB': DB,
            'INFLUXDB_ADMIN_USER': USER,
            'INFLUXDB_ADMIN_PASSWORD': PASSWORD
        }

    @classmethod
    def _wait_for_container_to_be_ready(cls):
        time.sleep(1)
        cls._wait_for_log_message('Listening on HTTP')
        time.sleep(1)

    @staticmethod
    def _get_container_name() -> str:
        return 'influxdb'

    @staticmethod
    def _get_ports() -> dict:
        return {'8086/tcp': '8086'}

    @staticmethod
    def _get_image_name() -> str:
        return 'influxdb:1.8-alpine'

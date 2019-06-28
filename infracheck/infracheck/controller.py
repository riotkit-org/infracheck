
from .runner import Runner
from .repository import Repository
from .config import ConfigLoader
from .server import HttpServer

import os
import time


class Controller:
    project_dirs = None   # type: list
    runner = None         # type: Runner
    repository = None     # type: Repository
    config_loader = None  # type: ConfigLoader
    server = None         # type: HttpServer

    def __init__(self, project_dir: str, server_port: int, server_path_prefix: str,
                 db_path: str, wait_time: int, lazy: bool, force: bool):

        self.project_dirs = self._combine_project_dirs(project_dir)
        self.runner = Runner(self.project_dirs)
        self.config_loader = ConfigLoader(self.project_dirs)
        self.repository = Repository(self.project_dirs, db_path)
        self.server = HttpServer(self, server_port, server_path_prefix, wait_time, lazy, force)

    def list_enabled_configs(self):
        return self.repository.get_configured_checks(with_disabled=False)

    def list_available_checks(self):
        return self.repository.get_available_checks()

    def list_all_configs(self):
        return self.repository.get_configured_checks(with_disabled=True)

    def spawn_server(self):
        return self.server.run()

    def perform_checks(self, force: bool, wait_time: int = 0, lazy=False):
        """
        :param force: Perform checks and write results
        :param wait_time: After each check wait (in seconds)
        :param lazy: If force not specified, and there is no result, then allow to perform a check on-demand
        :return:
        """

        configs = self.list_enabled_configs()
        results = {}
        global_status = True

        for config_name in configs:
            result = None

            if not force:
                cache = self.repository.retrieve_cache(config_name)

                if cache:
                    result = cache

            config = self.config_loader.load(config_name)

            if not result:
                if lazy or force:
                    result = self.runner.run(config['type'], config['input'], config.get('hooks', {}))
                    self.repository.push_to_cache(config_name, result)
                else:
                    result = ["Check not ready", False, ""]

            results[config_name] = {
                'status': result[1],
                'output': result[0],
                'hooks_output': result[2],
                'ident': config_name + '=' + str(result[1])
            }

            if not result[1]:
                global_status = False

            if force and wait_time > 0:
                time.sleep(wait_time)

        return {
            'checks': results,
            'global_status': global_status
        }

    @staticmethod
    def _combine_project_dirs(project_dir: str) -> list:
        paths = [
            # directory specified by eg. the "--directory" commandline parameter
            project_dir,

            # standalone application running from cloned repository
            os.path.dirname(os.path.realpath(__file__)) + '/../',

            # official docker container
            '/app',
            '/data',

            # current directory
            os.getcwd(),
        ]

        return list(filter(lambda path: os.path.isdir(path + '/configured'), paths))

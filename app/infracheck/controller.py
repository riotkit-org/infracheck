
from .runner import Runner
from .repository import Repository
from .config import ConfigLoader
from .server import HttpServer


class Controller:
    project_dirs = None   # type: list
    runner = None         # type: Runner
    repository = None     # type: Repository
    config_loader = None  # type: ConfigLoader
    server = None         # type: HttpServer

    def __init__(self, project_dir: str, server_port: int):
        self.project_dirs = self._combine_project_dirs(project_dir)
        self.runner = Runner(self.project_dirs)
        self.config_loader = ConfigLoader(self.project_dirs)
        self.repository = Repository(self.project_dirs)
        self.server = HttpServer(self, server_port)

    def list_enabled_configs(self):
        return self.repository.get_configured_checks(with_disabled=False)

    def list_available_checks(self):
        return self.repository.get_available_checks()

    def list_all_configs(self):
        return self.repository.get_configured_checks(with_disabled=True)

    def spawn_server(self):
        return self.server.run()

    def perform_checks(self):
        configs = self.list_enabled_configs()
        results = {}
        global_status = True

        for config_name in configs:
            config = self.config_loader.load(config_name)
            result = self.runner.run(config['type'], config['input'])

            results[config_name] = {
                'status': result[1],
                'output': result[0],
                'ident': config_name + '=' + str(result[1])
            }

            if not result[1]:
                global_status = False

        return {
            'checks': results,
            'status': global_status
        }

    @staticmethod
    def _combine_project_dirs(project_dir: str) -> list:
        return [project_dir]

import os
import sys
from typing import List
from .model import ExecutedChecksResultList
from .runner import Runner
from .repository import Repository
from .config import ConfigLoader
from .scheduler import Scheduler
from .versioning import get_version
from rkd.api.inputoutput import IO


class Controller(object):
    """
    Constructs application context and passes actions to given services that are taking care about the processing
    """

    project_dirs: list
    runner: Runner
    repository: Repository
    config_loader: ConfigLoader
    io: IO

    def __init__(self, project_dir: str, server_port: int, server_path_prefix: str,
                 db_path: str, wait_time: int, timeout: int, log_level: str):

        self.io = IO()
        self.io.set_log_level(log_level)
        self.project_dirs = self._combine_project_dirs(project_dir)
        self.config_loader = ConfigLoader(self.project_dirs)
        self.repository = Repository(self.project_dirs, db_path)

        self.runner = Runner(dirs=self.project_dirs, config_loader=self.config_loader,
                             repository=self.repository, timeout=timeout, wait_time=wait_time, io=self.io)

        self.scheduler = Scheduler(self.runner, self.repository, self.io)

    def list_enabled_configs(self) -> List[str]:
        return self.repository.get_configured_checks(with_disabled=False)

    def list_available_checks(self) -> List[str]:
        return self.repository.get_available_checks()

    def list_all_configs(self) -> List[str]:
        return self.repository.get_configured_checks(with_disabled=True)

    def spawn_threaded_application(self, refresh_time: int) -> None:
        """
        Spawns a background worker
        """

        self.scheduler.schedule_jobs_in_background(every_seconds=refresh_time)

    @staticmethod
    def get_version() -> dict:
        """
        Gets Infracheck version
        """

        return {
            "version": get_version(),
            "python": sys.version
        }

    def retrieve_checks(self) -> ExecutedChecksResultList:
        """
        Only retrieves results of last checking
        """

        return self.runner.get_checks_results(self.list_enabled_configs())

    def perform_checks(self) -> ExecutedChecksResultList:
        """
        Runs and returns results synchronously
        """

        configs = self.list_enabled_configs()

        self.runner.run_checks(configs)
        return self.runner.get_checks_results(configs)

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

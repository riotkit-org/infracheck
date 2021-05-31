
import inspect
import sys
import os

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.runner import Runner
from infracheck.infracheck.config import ConfigLoader
from infracheck.infracheck.repository import Repository
from infracheck.infracheck.model import ExecutedCheckResult, ConfiguredCheck
from rkd.api.inputoutput import IO


def run_check(check_type: str, input_data: dict, hooks: dict) -> ExecutedCheckResult:
    project_dirs = [path + '/../../example/healthchecks', path + '/../infracheck/']

    runner = Runner(project_dirs,
                    config_loader=ConfigLoader(project_dirs, IO()),
                    repository=Repository(project_dirs),
                    io=IO())

    return runner.run_single_check(ConfiguredCheck.from_config(
        'example-check', {
            'type': check_type,
            'input': input_data,
            'hooks': hooks
        },
        IO()
    ))

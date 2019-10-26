
import inspect
import sys
import os

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.runner import Runner


def run_check(check_type: str, input_data: dict, hooks: dict):
    runner = Runner([path + '/../../example/healthchecks', path + '/../infracheck/'])
    return runner.run(check_type, input_data, hooks)

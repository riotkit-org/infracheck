
import subprocess
import os
import json
import re
from datetime import datetime


class Runner:
    paths = []
    timeout: int

    def __init__(self, dirs, timeout: int = 1800):
        self.timeout = timeout

        for path in dirs:
            self.paths.append(path + '/checks')

    def run(self, check_name: str, input_data: dict, hooks: dict) -> tuple:
        bin_path = self._get_check_path(check_name)

        try:
            env = {**dict(os.environ), **self._prepare_data(check_name, input_data)}
            output = subprocess.check_output(bin_path, env=env, stderr=subprocess.PIPE, timeout=self.timeout)
            exit_status = True

        except subprocess.CalledProcessError as e:
            output = e.output + e.stderr
            exit_status = False

        hooks_out = self._notify_hooks(hooks, exit_status)

        return output.decode('utf-8'), exit_status, hooks_out

    @staticmethod
    def _prepare_data(check_name: str, input_data: dict):
        """ Serialize and parse """

        output_data = {}

        for key, value in input_data.items():
            if type(value) == dict or type(value) == list:
                value = json.dumps(value)

            output_data[key.upper()] = Runner._inject_variables(check_name, str(value))

        return output_data

    @staticmethod
    def _inject_variables(check_name: str, value: str) -> str:
        """ Inject variables, including environment variables from host,
            to allow for example secure passing of passwords"""

        matches = re.findall(r'\${([A-Za-z0-9_.]+)\}', value)

        if not matches:
            return value

        variables = {
            'checkName': check_name,
            'date': datetime.now().isoformat(),
        }

        for env_name, env_value in os.environ.items():
            variables['ENV.' + env_name.upper()] = env_value

        for match in matches:
            if match not in variables:
                raise Exception('Invalid variable "%s" in check %s. Available variables: %s' %
                                (match, check_name, str(variables.keys())))

            value = value.replace('${%s}' % match, variables[match])

        return value

    def _get_check_path(self, check_name: str):
        for path in self.paths:
            if os.path.isfile(path + '/' + check_name):
                return path + '/' + check_name

        raise Exception('Healthcheck executable "' + check_name + '" does not exist')

    @staticmethod
    def _notify_hooks(hooks: dict, exit_status: bool) -> str:
        mapping = {
            True: 'on_each_up',
            False: 'on_each_down'
        }

        out = ""

        if exit_status in mapping and mapping[exit_status] in hooks:
            commands = hooks[mapping[exit_status]]

            if type(commands).__name__ != 'list':
                raise Exception('Expected a LIST of hooks in "' + mapping[exit_status] + '"')

            for command in commands:
                out += subprocess.check_output(command, shell=True).decode('utf-8').strip()

        return out

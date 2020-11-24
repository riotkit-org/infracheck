
"""
Runner
======

Executes checks and captures result
"""

import subprocess
import os
import json
import re
import time
from datetime import datetime
from rkd.api.inputoutput import IO
from .exceptions import RunnerException
from .model import ExecutedCheckResult, ExecutedChecksResultList
from .repository import Repository
from .config import ConfigLoader
from .rkd_support import is_rkd_check, prepare_rkd_check_bin_path, add_rkd_environment_variables


class Runner(object):
    paths: list
    timeout: int
    wait_time: int
    config_loader: ConfigLoader
    repository: Repository
    io: IO

    def __init__(self, dirs: list, config_loader: ConfigLoader, repository: Repository, io: IO,
                 timeout: int = 1800, wait_time: int = 0):

        self.timeout = timeout
        self.wait_time = wait_time
        self.paths = []
        self.config_loader = config_loader
        self.repository = repository
        self.io = io

        for path in dirs:
            self.paths.append(path + '/checks')

    def run_single_check(self, configured_name: str, check_name: str, input_data: dict, hooks: dict) \
            -> ExecutedCheckResult:

        """
        Runs a single check and returns result

        :param configured_name:
        :param check_name:
        :param input_data:
        :param hooks:
        :return:
        """

        self.io.debug('Executing check {}'.format(configured_name))
        bin_path = self._get_check_path(check_name)
        bin_path = self._append_commandline_switches(input_data, bin_path)

        try:
            self.io.debug('bin_path=' + str(bin_path))

            env = {**dict(os.environ), **self._prepare_data(check_name, input_data)}
            env = self._add_environment_variables(env, check_name)

            timeout = env['INFRACHECK_TIMEOUT'] if 'INFRACHECK_TIMEOUT' in env else self.timeout

            output = subprocess.check_output(bin_path, env=env, stderr=subprocess.PIPE, timeout=timeout)
            exit_status = True

        except subprocess.CalledProcessError as e:
            output = e.output + e.stderr
            self.io.warn('{} returned error: {}'.format(configured_name, output.decode('utf-8')))
            exit_status = False

        except subprocess.TimeoutExpired as e:
            output = b'Timed out: '

            if e.output:
                output += e.output

            if e.stderr:
                output += e.stderr

            self.io.error('{} timed out and returned: {}'.format(configured_name, output))
            exit_status = False

        self.io.debug('Execution finished, running hooks...')
        hooks_out = self._notify_hooks(hooks, exit_status, self.io)

        return ExecutedCheckResult(
            output=output.decode('utf-8'),
            exit_status=exit_status,
            hooks_output=hooks_out,
            configured_name=configured_name
        )

    def run_checks(self, enabled_configs: list) -> None:
        """
        Runs checks one-by-one and saves to cache

        :param enabled_configs: List of enabled configuration files (json files)
        :return:
        """

        for config_name in enabled_configs:
            result = None
            config = self.config_loader.load(config_name)

            if not result:
                result = self.run_single_check(config_name, config['type'], config['input'], config.get('hooks', {}))
                self.repository.push_to_cache(config_name, result)

            if self.wait_time > 0:
                time.sleep(self.wait_time)

    def get_checks_results(self, enabled_configs: list) -> ExecutedChecksResultList:
        """
        Get results previously generated by runner

        :param enabled_configs:
        :return:
        """

        results = ExecutedChecksResultList()

        for config_name in enabled_configs:
            result = self.repository.retrieve_from_cache(config_name)

            if not result:
                result = ExecutedCheckResult.from_not_ready(configured_name=config_name)

            results.add(config_name, result)

        return results

    @staticmethod
    def _add_environment_variables(env: dict, check_name: str):
        if is_rkd_check(check_name):
            env = add_rkd_environment_variables(env, check_name)

        return env

    @staticmethod
    def _append_commandline_switches(input_data: dict, bin_path: list) -> list:
        """
        Inject commandline switches

        :param input_data:
        :param bin_path:
        :return:
        """

        for name, value in input_data.items():
            name: str

            if name.startswith('--'):
                bin_path.append(name + '=' + str(value))

            elif name.startswith('-'):
                bin_path.append(name)
                bin_path.append(str(value))

        return bin_path

    @staticmethod
    def _prepare_data(check_name: str, input_data: dict):
        """ Serialize and parse """

        output_data = {}

        for key, value in input_data.items():
            key: str

            if type(value) == dict or type(value) == list:
                value = json.dumps(value)

            if key.startswith('-'):
                continue

            output_data[key.upper()] = Runner._inject_variables(check_name, str(value))

        return output_data

    @staticmethod
    def _inject_variables(check_name: str, value: str) -> str:
        """
        Inject variables, including environment variables from host,
        to allow for example secure passing of passwords
        """

        matches = re.findall(r'\${([A-Za-z0-9_.]+)\}', value)

        if not matches:
            return value

        variables = {
            'checkName': check_name,
            'date': datetime.now().isoformat(),
            'timestamp': str(datetime.now().timestamp())
        }

        for env_name, env_value in os.environ.items():
            variables['ENV.' + env_name.upper()] = env_value

        for match in matches:
            if match not in variables:
                raise RunnerException.from_invalid_variable_error(match, check_name, variables)

            value = value.replace('${%s}' % match, variables[match])

        return value

    def _get_check_path(self, check_name: str) -> list:
        if is_rkd_check(check_name):
            return prepare_rkd_check_bin_path(check_name)

        for path in self.paths:
            if os.path.isfile(path + '/' + check_name):
                return [path + '/' + check_name]

        raise RunnerException.from_non_existing_executable(check_name)

    @staticmethod
    def _notify_hooks(hooks: dict, exit_status: bool, io: IO) -> str:
        mapping = {
            True: 'on_each_up',
            False: 'on_each_down'
        }

        out = ""

        if exit_status in mapping and mapping[exit_status] in hooks:
            commands = hooks[mapping[exit_status]]

            if type(commands).__name__ != 'list':
                raise RunnerException.from_expected_list_of_hooks(mapping[exit_status])

            for command in commands:
                io.debug('Triggering hook command "{}"'.format(command))

                try:
                    out += subprocess.check_output(command, shell=True, timeout=1800).decode('utf-8').strip()

                except subprocess.CalledProcessError as e:
                    io.error('Cannot execute hook command "{cmd}". Error: {err}'.format(
                        cmd=command, err=str(e.output) + str(e.stderr))
                    )
                except subprocess.TimeoutExpired:
                    io.error('Cannot execute hook command "{cmd}. Timed out while executing command"'.format(
                        cmd=command)
                    )
                except Exception:
                    io.error('Cannot execute hook command "{cmd}. Unknown error"'.format(cmd=command))

        return out

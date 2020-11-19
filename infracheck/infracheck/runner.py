
import subprocess
import os
import json
import re
import time
from datetime import datetime
from .model import ExecutedCheckResult, ExecutedChecksResultList
from .repository import Repository
from .config import ConfigLoader
from rkd.api.inputoutput import IO


class Runner(object):
    """
    Runs a configured check
    """

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

    def run(self, configured_name: str, check_name: str, input_data: dict, hooks: dict) -> ExecutedCheckResult:
        self.io.debug('Executing check {}'.format(configured_name))
        bin_path = self._get_check_path(check_name)

        try:
            env = {**dict(os.environ), **self._prepare_data(check_name, input_data)}
            timeout = env['INFRACHECK_TIMEOUT'] if 'INFRACHECK_TIMEOUT' in env else self.timeout

            output = subprocess.check_output(bin_path, env=env, stderr=subprocess.PIPE, timeout=timeout)
            exit_status = True

        except subprocess.CalledProcessError as e:
            output = e.output + e.stderr
            exit_status = False
        except subprocess.TimeoutExpired as e:
            output = b'Timed out: ' + ((str(e.output) + str(e.stderr)).encode('utf-8'))
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
                result = self.run(config_name, config['type'], config['input'], config.get('hooks', {}))
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
                # @todo: Refactor exception class
                raise Exception('Invalid variable "%s" in check %s. Available variables: %s' %
                                (match, check_name, str(variables.keys())))

            value = value.replace('${%s}' % match, variables[match])

        return value

    def _get_check_path(self, check_name: str):
        for path in self.paths:
            if os.path.isfile(path + '/' + check_name):
                return path + '/' + check_name

        # @todo: Refactor exception class
        raise Exception('Healthcheck executable "' + check_name + '" does not exist')

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
                raise Exception('Expected a LIST of hooks in "' + mapping[exit_status] + '"')

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

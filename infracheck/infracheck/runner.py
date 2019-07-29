
import subprocess
import os


class Runner:
    paths = []

    def __init__(self, dirs):
        for path in dirs:
            self.paths.append(path + '/checks')

    def run(self, check_name: str, input_data: dict, hooks: dict) -> tuple:
        bin_path = self._get_check_path(check_name)

        try:
            env = {**dict(os.environ), **self._prepare_data(input_data)}
            output = subprocess.check_output(bin_path, env=env, stderr=subprocess.PIPE)
            exit_status = True

        except subprocess.CalledProcessError as e:
            output = e.output + e.stderr
            exit_status = False

        hooks_out = self._notify_hooks(hooks, exit_status)

        return output.decode('utf-8'), exit_status, hooks_out

    @staticmethod
    def _prepare_data(input_data: dict):
        output_data = {}

        for key, value in input_data.items():
            output_data[key.upper()] = str(value)

        return output_data

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

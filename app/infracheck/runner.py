
import subprocess
import os


class Runner:
    paths = []

    def __init__(self, dirs):
        for path in dirs:
            self.paths.append(path + '/checks')

    def run(self, check_name: str, input_data: dict) -> tuple:
        bin_path = self._get_check_path(check_name)

        try:
            env = {**dict(os.environ), **self._prepare_data(input_data)}
            output = subprocess.check_output(bin_path, env=env, stderr=subprocess.PIPE)
            exit_status = True

        except subprocess.CalledProcessError as e:
            output = e.output
            exit_status = False

        return output.decode('utf-8'), exit_status

    @staticmethod
    def _prepare_data(input_data: dict):
        output_data = {}

        for key, value in input_data.items():
            output_data[key.upper()] = value

        return output_data

    def _get_check_path(self, check_name: str):
        for path in self.paths:
            if os.path.isfile(path + '/' + check_name):
                return path + '/' + check_name

        return '/bin/false'

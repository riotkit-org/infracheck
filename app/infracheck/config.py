
import os
import json


class ConfigLoader:
    paths = []

    def __init__(self, paths):
        self.paths = paths

    def load(self, config_name: str) -> dict:
        file_path = self._find_file_path('/configured/', config_name, '.json')

        if not file_path:
            raise FileNotFoundError('Configuration file not found for "' + config_name + '"')

        handle = open(file_path, 'rb')
        content = handle.read()
        handle.close()

        data = json.loads(content)

        self._assert_valid_format(config_name, data)
        self._assert_has_valid_type(str(data['type']))

        return data

    @staticmethod
    def _assert_valid_format(config_name: str, data):
        if "type" not in data:
            raise Exception('Configuration "' + config_name + '" needs to specify a name of a check in field "type"')

    def _assert_has_valid_type(self, type_name: str):
        if not self._find_file_path('/checks/', type_name, ''):
            raise Exception('Invalid check type "' + type_name + '", was looking in: ' + str(self.paths))

        return

    def _find_file_path(self, dir_name: str, config_name: str, suffix: str) -> str:
        for path in self.paths:
            if os.path.isfile(path + dir_name + config_name + suffix):
                return path + dir_name + config_name + suffix

        return ''


"""
Config
======

Configuration locator and loader, loads JSON objects from disk and returns ConfigurationCheck models.
Searches through hierarchy of paths defined in controller.Controller._combine_project_dirs()
"""

import os
import json
from dataclasses import dataclass
from typing import List
from rkd.api.inputoutput import IO
from .exceptions import ConfigurationException
from .model import ConfiguredCheck
from .rkd_support import is_rkd_check, rkd_module_exists


@dataclass
class ConfigLoader(object):
    paths: List[str]
    io: IO

    def load(self, config_name: str) -> ConfiguredCheck:
        file_path = self._find_file_path('/configured/', config_name, '.json')

        if not file_path:
            raise FileNotFoundError('Configuration file not found for "' + config_name + '"')

        handle = open(file_path, 'rb')
        content = handle.read()
        handle.close()

        data = json.loads(content)

        self._assert_valid_format(config_name, data)
        self._assert_has_valid_type(str(data['type']))

        return ConfiguredCheck.from_config(config_name, data, self.io)

    @staticmethod
    def _assert_valid_format(config_name: str, data):
        if "type" not in data:
            raise Exception('Configuration "' + config_name + '" needs to specify a name of a check in field "type"')

    def _assert_has_valid_type(self, type_name: str):
        if is_rkd_check(type_name):
            if not rkd_module_exists(type_name):
                raise ConfigurationException.from_rkd_module_not_existing(type_name)

            return True

        if not self._find_file_path('/checks/', type_name, ''):
            raise ConfigurationException.from_binary_not_found(type_name, self.paths)

        return

    def _find_file_path(self, dir_name: str, config_name: str, suffix: str) -> str:
        for path in self.paths:
            if os.path.isfile(path + dir_name + config_name + suffix):
                return path + dir_name + config_name + suffix

        return ''

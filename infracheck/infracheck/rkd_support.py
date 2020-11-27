"""
RKD Support
===========

Methods used to add RiotKit-Do support in the InfraCheck
"""

import sys
from typing import Tuple

from rkd.exception import ParsingException
from rkd.api.contract import TaskDeclarationInterface
from rkd.api.parsing import SyntaxParsing
from .exceptions import ConfigurationException


def is_rkd_check(check_name: str) -> bool:
    schema_length = len('rkd://')

    if not check_name[0:schema_length] == 'rkd://':
        return False

    return ":" in check_name[schema_length:]


def split_rkd_path(check_name: str) -> Tuple[str, str]:
    if not is_rkd_check(check_name):
        raise ConfigurationException.from_rkd_check_url_error(check_name)

    module_name, task_name = check_name[len('rkd://'):].split(':', 1)

    return module_name, ':' + task_name


def prepare_rkd_check_bin_path(check_name: str) -> list:
    module_name, task_name = split_rkd_path(check_name)

    return [sys.executable, '-m', 'rkd', '--imports', module_name, task_name]


def rkd_module_exists(check_name: str) -> bool:
    module_name, task_name = split_rkd_path(check_name)

    try:
        tasks = SyntaxParsing.parse_imports_by_list_of_classes([module_name])

    except ParsingException:
        return False

    for task in tasks:
        task: TaskDeclarationInterface

        if task.get_task_to_execute().get_name() == task_name:
            return True

    return False


def add_rkd_environment_variables(env: dict, check_name: str) -> dict:
    env['RKD_UI'] = 'false'

    return env

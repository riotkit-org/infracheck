from typing import Dict


class RunnerException(Exception):
    @staticmethod
    def from_invalid_variable_error(var_name: str, check_name: str, available_vars: Dict[str, str]) \
            -> 'RunnerException':

        return RunnerException(
            'Invalid variable "%s" in check %s. Available variables: %s' %
            (var_name, check_name, str(available_vars.keys()))
        )

    @staticmethod
    def from_non_existing_executable(check_name: str) -> 'RunnerException':
        return RunnerException('Healthcheck executable "{check_name}" does not exist'.format(check_name=check_name))

    @staticmethod
    def from_expected_list_of_hooks(hook_name: str):
        return RunnerException('Expected a LIST of hooks in "{hook_name}"'.format(hook_name=hook_name))

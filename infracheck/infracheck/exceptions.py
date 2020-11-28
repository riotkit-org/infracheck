from typing import Dict


class InfracheckException(Exception):
    pass


class RunnerException(InfracheckException):
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


class ConfigurationException(InfracheckException):
    @classmethod
    def from_rkd_module_not_existing(cls, check_name: str) -> 'ConfigurationException':
        return cls(
            'RKD module cannot be imported, or task name is invalid: {check_name}'.format(check_name=check_name)
        )

    @classmethod
    def from_binary_not_found(cls, check_name: str, paths: list) -> 'ConfigurationException':
        return cls(
            'Invalid check type "{check_name}", was looking in: "{paths}"'.format(
                check_name=check_name,
                paths=str(paths)
            )
        )

    @classmethod
    def from_rkd_check_url_error(cls, check_name):
        return cls(
            'RiotKit-Do check syntax "{}" is invalid. Valid example: rkd://rkd.standardlib.shell:sh'.format(check_name)
        )

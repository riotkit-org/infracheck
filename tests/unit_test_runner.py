import unittest
import sys
import os
import inspect
from unittest_data_provider import data_provider

TESTS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, TESTS_PATH)

from infracheck.infracheck.runner import Runner
from infracheck.infracheck.config import ConfigLoader
from infracheck.infracheck.repository import Repository
from rkd.api.inputoutput import IO


class RunnerTest(unittest.TestCase):
    def provide_data():
        return [
            # url does not exist: will return False
            [
                'http',
                {
                    'url': 'https://duckduckgo-some-invalid-domain.com'
                },
                {
                    'on_each_up': ['echo "is up"'],
                    'on_each_down': ['echo "is down"']
                },
                False,
                'is down'
            ],

            # valid HTTP health check
            # checks also if the on_each_up hook is called
            [
                'http',
                {
                    'url': 'https://duckduckgo.com'
                },
                {
                    'on_each_up': ['echo "it works"'],
                    'on_each_down': ['echo "this should not show"']
                },
                True,
                'it works'
            ],
        ]

    @data_provider(provide_data)
    def test_run_with_hooks(self, check_type: str, input_data: dict, hooks: dict, expected_result: bool, expected_text: str):
        result = self._create_runner().run_single_check('some-check-name', check_type, input_data, hooks)

        self.assertEqual(expected_result, result.exit_status)
        self.assertEqual(expected_text, result.hooks_output)

    def test_injects_variables(self):
        out = self._create_runner().run_single_check(
            configured_name='some-check-name',
            check_name='printr',
            input_data={'message': 'Current user is ${ENV.USER}, running a ${checkName}'},
            hooks={}
        )

        self.assertEqual('Current user is ' + os.environ['USER'] + ', running a printr', out.output.strip())

    @staticmethod
    def _create_runner() -> Runner:
        dirs = [TESTS_PATH + '/../example/healthchecks', TESTS_PATH + '/infracheck/']

        return Runner(dirs,
                      config_loader=ConfigLoader(dirs),
                      repository=Repository(dirs),
                      io=IO())

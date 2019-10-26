import unittest
import sys
import os
import inspect
from unittest_data_provider import data_provider

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.append(path)

try:
    from .infracheck.infracheck.runner import Runner
except ImportError as e:
    from infracheck.infracheck.runner import Runner


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
            ]
        ]

    @data_provider(provide_data)
    def test_run(self, type: str, input_data: dict, hooks: dict, expected_result: bool, expected_text: str):
        runner = Runner([path + '/../example/healthchecks', path])
        out = runner.run(type, input_data, hooks)

        self.assertEqual(expected_result, out[1])
        self.assertEqual(expected_text, out[2])

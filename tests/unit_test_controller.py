import unittest
import sys
import os
import inspect
from unittest import mock
from unittest_data_provider import data_provider

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.append(path)

from infracheck.infracheck.controller import Controller


class ControllerTest(unittest.TestCase):

    def provide_data():
        return [
            # File is present, with hooks, success path
            [
                # config
                {
                    "type": "file-present",
                    "input": {
                        "file_path": "/bin/sh"
                    },
                    "hooks": {
                        "on_each_up": [
                            "echo 'Yeeeah'",
                            "echo ', is up'"
                        ],
                        "on_each_down": [
                            "echo 'This should'",
                            "echo 'not show'"
                        ]
                    }
                },
                # expected result
                True,
                # expected ident
                'example-check=True',
                # expected hooks output
                'Yeeeah, is up'
            ],

            # File is present, with hooks, success path
            [
                # config
                {
                    "type": "file-present",
                    "input": {
                        "file_path": "/bin/non-existent-file"
                    },
                    "hooks": {
                        "on_each_up": [
                            "echo 'Yeeeah'",
                            "echo ', is up'"
                        ],
                        "on_each_down": [
                            "echo 'Oops!'",
                        ]
                    }
                },
                # expected result
                False,
                # expected ident
                'example-check=False',
                # expected hooks output
                'Oops!'
            ],

            # HTTP check for google.com without hooks
            [
                # config
                {
                    "type": "http",
                    "input": {
                        "url": "https://google.com"
                    }
                },
                # expected result
                True,
                # expected ident
                'example-check=True',
                # expected hooks output
                ''
            ],

            # HTTP check with expectation keywords
            [
                # config
                {
                    "type": "http",
                    "input": {
                        "url": "https://duckduckgo.com",
                        'expect_keyword': 'DOCTYPE',
                        'not_expect_keyword': 'something that should not show on this page'
                    }
                },
                # expected result
                True,
                # expected ident
                'example-check=True',
                # expected hooks output
                ''
            ],

            # HTTP: Call address that does not exist (DNS failure)
            [
                # config
                {
                    "type": "http",
                    "input": {
                        "url": "http://sooomeadasdsdads"
                    }
                },
                # expected result
                False,
                # expected ident
                'example-check=False',
                # expected hooks output
                ''
            ],

            # HTTP: Call non-existing page
            [
                # config
                {
                    "type": "http",
                    "input": {
                        "url": "https://httpstat.us/404"
                    }
                },
                # expected result
                False,
                # expected ident
                'example-check=False',
                # expected hooks output
                ''
            ]
        ]

    @data_provider(provide_data)
    def test_simply_perform_checks(self, config: dict, expected_result: bool, expected_ident: str,
                                   expected_hooks_output: str):
        controller = Controller(
            project_dir=path,
            server_port=8000,
            server_path_prefix='',
            db_path='/tmp/.infracheck.sqlite3',
            wait_time=0,
            lazy=True,
            force=True
        )

        # mocks
        controller.list_enabled_configs = get_enabled_configs_mock
        controller.config_loader.load = mock.Mock()

        with mock.patch.object(controller.config_loader, 'load', return_value=config):
            performed = controller.perform_checks(force=True, lazy=True)

        self.assertEqual(expected_result, performed['checks']['example-check']['status'])

        # ident - important for monitoring
        self.assertEqual(expected_ident, performed['checks']['example-check']['ident'])

        # hooks for notifying
        self.assertEqual(expected_hooks_output, performed['checks']['example-check']['hooks_output'])


def get_enabled_configs_mock():
    return ['example-check']


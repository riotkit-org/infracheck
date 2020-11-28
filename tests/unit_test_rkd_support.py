import unittest
import sys
import os
import inspect

TESTS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, TESTS_PATH)

from infracheck.infracheck.rkd_support import *


class RkdSupportTest(unittest.TestCase):
    def test_is_rkd_check(self):
        """
        Checks if RKD "url" has correct format
        """

        with self.subTest('Empty url'):
            self.assertFalse(is_rkd_check(''))

        with self.subTest('Empty url - only schema present'):
            self.assertFalse(is_rkd_check('rkd://'))

        with self.subTest('Url with only import name, without task name'):
            self.assertFalse(is_rkd_check('rkd://rkd.standardlib.shell'))

        with self.subTest('Fully complete url'):
            self.assertTrue(is_rkd_check('rkd://rkd.standardlib.shell:sh'))

    def test_split_rkd_path(self):
        """
        Splits URL into module and task names
        """

        self.assertEqual(
            ('rkd.standardlib.shell', ':test'),
            split_rkd_path('rkd://rkd.standardlib.shell:test')
        )

    def test_prepare_rkd_check_bin_path(self):
        self.assertIn(
            "'-m', 'rkd', '--imports', 'rkd.standardlib.shell', ':test'",
            str(prepare_rkd_check_bin_path('rkd://rkd.standardlib.shell:test'))
        )

    def test_rkd_module_exists(self):
        with self.subTest('Success case - module and task are found'):
            self.assertTrue(rkd_module_exists('rkd://rkd.standardlib.shell:sh'))

        with self.subTest('Failure case - module not found'):
            self.assertFalse(rkd_module_exists('rkd://rkd.standardlib.not_existing_name:sh'))

        with self.subTest('Failure case - task not found in module'):
            self.assertFalse(rkd_module_exists('rkd://rkd.standardlib.shell:non-existing-task'))

    def test_add_rkd_environment_variables(self):
        self.assertEqual({'RKD_UI': 'false'}, add_rkd_environment_variables({}, 'test'))

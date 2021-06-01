import os
import sys
import inspect
from rkd.api.inputoutput import IO
from rkd.api.testing import BasicTestingCase


TESTS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, TESTS_PATH)

from infracheck.infracheck.config import ConfigLoader


class ConfigTest(BasicTestingCase):
    def test_load_finds_file_successfully(self):
        """
        Loads a check configuration with a success
        """

        loader = ConfigLoader([TESTS_PATH + '/example/healthchecks', TESTS_PATH + '/infracheck'], IO())
        check = loader.load('ram')

        self.assertEqual('ram', check.name)
        self.assertEqual('85', check.input_variables.get('max_ram_percentage'))

    def test_load_does_not_find_file(self):
        loader = ConfigLoader([TESTS_PATH + '/example/healthchecks', TESTS_PATH + '/infracheck'], IO())

        self.assertRaises(FileNotFoundError, lambda: loader.load('not-existing'))

    def test_assert_valid_format(self):
        with self.subTest('Success case'):
            ConfigLoader._assert_valid_format('Durruti', {'type': 'curl'})

        with self.subTest('Failure case - missing "type" attribute'):
            self.assertRaises(Exception, lambda: ConfigLoader._assert_valid_format('Some', {}))

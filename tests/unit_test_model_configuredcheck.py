import unittest
import sys
import os
import inspect
from datetime import datetime
from rkd.api.inputoutput import IO

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.model import ConfiguredCheck
from infracheck.infracheck.exceptions import ConfigurationException


class ConfiguredCheckTest(unittest.TestCase):
    def test_factory_checks_quiet_period_type(self):
        with self.assertRaises(ConfigurationException) as exc:
            ConfiguredCheck.from_config(
                name='test',
                config={
                    'quiet_periods': ''
                },
                io=IO()
            )

        self.assertEqual(
            '"quiet_periods" should be a list',
            str(exc.exception)
        )

    def test_factory_checks_quiet_period_dictionary_keys(self):
        with self.assertRaises(ConfigurationException) as exc:
            ConfiguredCheck.from_config(
                name='test',
                config={
                    'quiet_periods': [
                        {}
                    ]
                },
                io=IO()
            )

        self.assertEqual(
            '"quiet_periods" contains invalid structure. Valid entry example: '
            '{"starts": "30 00 * * *", "duration": 60}',
            str(exc.exception)
        )

    def test_factory_allows_empty_quiet_period(self):
        check = ConfiguredCheck.from_config(
            name='test',
            config={
                'quiet_periods': []  # empty list
            },
            io=IO()
        )

        # no exception is raised, object is returned
        self.assertEqual('test', check.name)

    def test_should_signal_that_quiet_period_is_now_case_middle_of_time(self):
        """
        06:00 - 06:30
        Case: 06:15
        """
        check = self._create_check_with_quiet_period('00 06 * * *', 30)

        # mock the current time
        check._time_now = lambda: datetime(year=1922, month=12, day=25, hour=6, minute=15, second=0)

        self.assertTrue(check.should_status_be_ignored())

    def test_should_signal_that_quiet_period_is_now_case_when_time_equals_the_border_value(self):
        """
        06:00 - 06:30, Case: 06:30
        """

        check = self._create_check_with_quiet_period('00 06 * * *', 30)

        # mock the current time
        check._time_now = lambda: datetime(year=1910, month=11, day=1, hour=6, minute=30, second=0)

        self.assertTrue(check.should_status_be_ignored())

    def test_should_signal_that_quiet_period_is_now_case_when_time_equals_the_border_value_at_the_beginning(self):
        """
        06:00 - 06:30, Case: 06:00
        """

        check = self._create_check_with_quiet_period('00 06 * * *', 30)

        # mock the current time
        check._time_now = lambda: datetime(year=1936, month=7, day=18, hour=6, minute=0, second=0)

        self.assertTrue(check.should_status_be_ignored())

    def test_should_not_signal_even_1_minute_after(self):
        """
        06:00 - 06:30, Case: 06:31
        """

        check = self._create_check_with_quiet_period('00 06 * * *', 30)

        # mock the current time
        check._time_now = lambda: datetime(year=2050, month=5, day=1, hour=6, minute=31, second=0)

        self.assertFalse(check.should_status_be_ignored())

    def test_should_not_signal_before_period_starts(self):
        """
        06:00 - 06:30, Case: 05:59
        """

        check = self._create_check_with_quiet_period('00 06 * * *', 30)

        # NOW = in the middle of the quiet period time
        check._time_now = lambda: datetime(year=2161, month=5, day=1, hour=5, minute=59, second=0)

        self.assertFalse(check.should_status_be_ignored())

    @staticmethod
    def _create_check_with_quiet_period(starts: str, duration: int) -> ConfiguredCheck:
        return ConfiguredCheck.from_config(
            name='test',
            config={
                'quiet_periods': [
                    {'starts': starts, 'duration': duration}
                ]
            },
            io=IO()
        )

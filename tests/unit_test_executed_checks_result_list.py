import sys
import os
import inspect
from rkd.api.testing import BasicTestingCase

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.model import ExecutedChecksResultList, ExecutedCheckResult


class ExecutedChecksResultListTest(BasicTestingCase):
    def test_is_global_status_success(self):
        """
        Checks if global status of the endpoint works as expected in basing on checks results
        """

        with self.subTest('One check is failing, then global status is failure'):
            results = ExecutedChecksResultList()
            results.add('first', ExecutedCheckResult(
                configured_name='first',
                output='Test',
                exit_status=False,
                hooks_output=''
            ))
            results.add('second', ExecutedCheckResult(
                configured_name='second',
                output='Test',
                exit_status=True,
                hooks_output=''
            ))

            self.assertFalse(results.is_global_status_success())

        with self.subTest('All checks are passing, then we have a success'):
            results = ExecutedChecksResultList()
            results.add('first', ExecutedCheckResult(
                configured_name='first',
                output='Test',
                exit_status=True,
                hooks_output=''
            ))
            results.add('second', ExecutedCheckResult(
                configured_name='second',
                output='Test',
                exit_status=True,
                hooks_output=''
            ))

            self.assertTrue(results.is_global_status_success())

        with self.subTest('All checks are failing, then we have a failure'):
            results = ExecutedChecksResultList()
            results.add('first', ExecutedCheckResult(
                configured_name='first',
                output='Test',
                exit_status=False,
                hooks_output=''
            ))
            results.add('second', ExecutedCheckResult(
                configured_name='second',
                output='Test',
                exit_status=False,
                hooks_output=''
            ))

            self.assertFalse(results.is_global_status_success())

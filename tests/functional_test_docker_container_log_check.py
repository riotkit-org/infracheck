import unittest
import os
import inspect
from typing import Tuple

# import a script with "-" in filename
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
with open(path + '/infracheck/checks/docker-container-log', 'r') as script:
    exec(script.read())


class DockerContainerLogCheckTest(unittest.TestCase):
    @staticmethod
    def _run_mocked_check(container: str, regexp: str, max_lines: int, since: int, should_be_present: bool) \
            -> Tuple[bool, str, list]:

        check = DockerContainerLogCheck()
        called = []

        def check_output(*args, **kwargs):
            called.append(args)

            return b"""
            Hello
            World
            
            This
            Is
            A
            Test
            """

        check._check_output = check_output
        result, message = check.main(
            container,
            regexp,
            max_lines,
            since,
            should_be_present
        )

        return result, message, called

    def test_expecting_exact_match_and_have_match(self) -> None:
        result, message, called = self._run_mocked_check(
            container='container_1',
            regexp='Hello',
            max_lines=15,
            since=5,
            should_be_present=True
        )

        self.assertTrue(result)
        self.assertEqual('The container last 15 lines of output has a match, as expected', message)

    def test_expecting_that_will_not_match(self) -> None:
        result, message, called = self._run_mocked_check(
            container='container_1',
            regexp='This text will not be found',
            max_lines=15,
            since=5,
            should_be_present=True
        )

        self.assertFalse(result)
        self.assertEqual('The container last 15 lines of output are not matching, expecting they were', message)

    def test_expecting_to_not_find_text_and_will_not_find(self) -> None:
        result, message, called = self._run_mocked_check(
            container='container_1',
            regexp='This text will not be found',
            max_lines=15,
            since=5,
            should_be_present=False
        )

        self.assertTrue(result)
        self.assertEqual('The container last 15 lines of output are not matching, as expected', message)

    def test_expecting_to_not_find_but_will_find(self) -> None:
        result, message, called = self._run_mocked_check(
            container='container_1',
            regexp='Hello',
            max_lines=15,
            since=5,
            should_be_present=False
        )

        self.assertFalse(result)
        self.assertEqual('The container output is matching the pattern but should not, '
                         'looked at 15 lines since 5s in container_1', message)

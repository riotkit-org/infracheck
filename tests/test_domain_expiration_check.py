import unittest
import os
import inspect
import unittest.mock
import datetime

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../infracheck/checks/'
DomainCheck: any
filename = path + '/domain-expiration'
exec(compile(open(filename, "rb").read(), filename, 'exec'))


class WhoIsMock:
    expiration_date: datetime

    def __init__(self, expiration_date: datetime):
        self.expiration_date = expiration_date


class DomainExpirationCheckTest(unittest.TestCase):
    def test_ok(self):
        check = DomainCheck('google.com', 25)

        with unittest.mock.patch.object(check, 'whois') as whois_mocked:
            whois_mocked.query.return_value = WhoIsMock(
                datetime.datetime.now() + datetime.timedelta(days=161)
            )
            result = check.perform_check()

        self.assertIn("is not expired", result[1])
        self.assertTrue(result[0])

    def test_not_registered(self):
        check = DomainCheck('dijweqjiqewjioqewjioqwejiqeij-not-exists.com', 25)
        result = check.perform_check()

        self.assertIn("Domain seems to be not registered", result[1])
        self.assertFalse(result[0])

    def test_expired(self):
        check = DomainCheck('google.com', 25)

        with unittest.mock.patch.object(check, 'whois') as whois_mocked:
            whois_mocked.query.return_value = WhoIsMock(datetime.datetime.now())

            result = check.perform_check()

        self.assertIn("Domain google.com expired", result[1])
        self.assertFalse(result[0])

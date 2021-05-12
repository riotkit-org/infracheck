#!/usr/bin/python3

import os
import inspect
from unittest import TestCase

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../infracheck/checks/'
TlsCheck: any
filename = path + '/tls'
exec(compile(open(filename, "rb").read(), filename, 'exec'))


class UnitTestTlsCheck(TestCase):
    def test_certificate_is_expiring(self) -> None:
        check = TlsCheck()
        check.get_certificate_expiration_date = lambda domain, host, port: ("Jul 31 23:59:59 1990 GMT", "...")

        exit_code, message = check.main(domain='', host='', port=443, alert_days_before=1)
        self.assertIn('Certificate is expiring soon, only', message)
        self.assertEqual(1, exit_code)

    def test_certificate_not_expired(self) -> None:
        check = TlsCheck()
        check.get_certificate_expiration_date = lambda domain, host, port: ("Jul 31 23:59:59 2999 GMT", "...")

        exit_code, message = check.main(domain='', host='', port=443, alert_days_before=1)
        self.assertEqual(0, exit_code)
        self.assertEqual('Certificate valid until Jul 31 23:59:59 2999 GMT', message)

    def test_certificate_invalid_format_returned_by_openssl(self) -> None:
        check = TlsCheck()
        check.get_certificate_expiration_date = lambda domain, host, port: ("sometime", "...")

        exit_code, message = check.main(domain='', host='', port=443, alert_days_before=1)
        self.assertEqual(1, exit_code)
        self.assertIn("Error parsing date - invalid format returned by OpenSSL binary 'sometime'", message)

    def test_invalid_openssl_output_is_catch(self) -> None:
        check = TlsCheck()

        exit_code, message = check.main(domain='localhost', host='localhost', port=9999, alert_days_before=1)
        self.assertIn('Error parsing date - invalid format returned by OpenSSL binary', message)

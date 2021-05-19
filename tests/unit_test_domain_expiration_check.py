import unittest
import os
import inspect
import unittest.mock
import datetime
import whois

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

    def test_sk_domain_manual_whois_parsing(self):
        check = DomainCheck('priamaakcia.sk', 25)

        def mock_library_raises_exception(*args, **kwargs):
            raise whois.exceptions.UnknownTld()

        check._ask_whois_library = mock_library_raises_exception
        check._ask_whois_in_shell = lambda *args, **kwargs: """
            Domain:                       priamaakcia.sk
            Registrant:                   WEBHOUSE-AZPNWEY
            Admin Contact:                WEBHOUSE
            Tech Contact:                 WEBHOUSE
            Registrar:                    IPEK-0001
            Created:                      2005-06-24
            Updated:                      2020-07-08
            Valid Until:                  2999-06-24
            Nameserver:                   ns1.afraid.org
            Nameserver:                   ns2.afraid.org
            EPP Status:                   ok
            
            Registrar:                    IPEK-0001
            Name:                         WebHouse, s.r.o.
            Organization:                 WebHouse, s.r.o.
            Organization ID:              36743852
            Phone:                        +421.332933500
            Email:                        domeny@webhouse.sk
            Street:                       Paulínska 20
            City:                         Trnava
            Postal Code:                  91701
            Country Code:                 SK
            Created:                      2017-09-01
            Updated:                      2021-05-17
            
            Contact:                      WEBHOUSE-AZPNWEY
            Registrar:                    IPEK-0001
            Created:                      2017-09-02
            Updated:                      2017-11-01
            
            Contact:                      WEBHOUSE
            Name:                         WebHouse, s. r. o.
            Organization:                 WebHouse, s. r. o.
            Organization ID:              36743852
            Phone:                        +421.910969601
            Email:                        domeny@webhouse.sk
            Street:                       Paulínska 20
            City:                         Trnava
            Postal Code:                  917 01
            Country Code:                 SK
            Registrar:                    IPEK-0001
            Created:                      2017-09-02
            Updated:                      2021-03-22
        """

        result = check.perform_check()

        self.assertIn('Domain priamaakcia.sk is not expired.', result[1])
        self.assertTrue(result[0])

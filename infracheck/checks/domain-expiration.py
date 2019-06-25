#!/usr/bin/env python3

"""
    Checks if the domain is close to expiration date or if already expired
"""

import whois
import datetime
import pytz
import os
import sys


class DomainCheck:
    _domain: str
    _alert_days_before: int

    def __init__(self, domain: str, alert_days_before: int):
        self._domain = domain
        self._alert_days_before = alert_days_before

        if not self._domain or self._domain == '':
            raise Exception('Domain must be specified')

    def perform_check(self) -> tuple:
        domain_check = whois.query(self._domain)

        try:
            exp_date = pytz.utc.localize(domain_check.expiration_date)
        except ValueError:
            exp_date = domain_check.expiration_date

        alert_begins = exp_date + datetime.timedelta(days=self._alert_days_before * -1)
        now = pytz.utc.localize(datetime.datetime.now())
        delta = exp_date - now

        if now >= exp_date:
            return False, "Domain {} expired at {}!".format(self._domain, exp_date.strftime('%Y-%M-%D'))

        if now >= alert_begins:

            return False, "The domain will expire soon in {} days".format(delta.days)

        return True, "Domain {} is not expired. {} days left".format(self._domain, delta.days)


if __name__ == '__main__':
    check = DomainCheck(os.getenv('DOMAIN', ''), os.getenv('ALERT_DAYS_BEFORE', 20))
    result = check.perform_check()

    print(result[1])
    sys.exit(0 if result[0] else 1)

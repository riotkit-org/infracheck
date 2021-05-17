#!/usr/bin/python3

import os
import warnings
import inspect
from unittest import TestCase
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../infracheck/checks/'
TlsDockerNetworkCheck: any
filename = path + '/tls-docker-network'
exec(compile(open(filename, "rb").read(), filename, 'exec'))


class FunctionalTestTlsDockerNetwork(TestCase):
    def setUp(self):
        warnings.simplefilter("ignore")

    def test_multiple_containers_with_multiple_domains_per_container(self):
        """
        There are two containers. Matching is by environment variable INFR_VIRTUAL_HOST={{ domain }}
        One with single domain: google.com
        Second one: duckduck.com and bing.com

        Checks:
            - There is a correct connection to docker, and proper parsing of the data from docker
            - "tls" check is correctly called
        """

        first = DockerContainer(image='nginx:1.19').with_env('INFR_VIRTUAL_HOST', 'duckduckgo.com,bing.com').start()
        second = DockerContainer(image='nginx:1.19').with_env('INFR_VIRTUAL_HOST', 'google.com').start()

        try:
            wait_for_logs(first, 'ready for start up')
            wait_for_logs(second, 'ready for start up')

            os.environ['PATH'] = path + ':' + os.environ['PATH']
            check = TlsDockerNetworkCheck(param_type='environment', param_name='INFR_VIRTUAL_HOST', alert_days_before=1)\
                .main()

        finally:
            first.stop()
            second.stop()

        self.assertIn('Domain google.com is OK', check[0])
        self.assertIn('Domain bing.com is OK', check[0])
        self.assertIn('Domain duckduckgo.com is OK', check[0])
        self.assertTrue(check[1])

    def test_containers_matched_by_label(self):
        """
        There are two docker containers. Matching is by label org.riotkit.domain: {{ domain }}

        Checks:
            - Parsing of the labels syntax
        """

        first = DockerContainer(image='nginx:1.19').with_kwargs(labels={'org.riotkit.domain': 'duckduckgo.com'}).start()
        second = DockerContainer(image='nginx:1.19')\
            .with_kwargs(labels={'org.riotkit.domain': 'riseup.net,bing.com'}).start()

        try:
            wait_for_logs(first, 'ready for start up')
            wait_for_logs(second, 'ready for start up')

            os.environ['PATH'] = path + ':' + os.environ['PATH']
            check = TlsDockerNetworkCheck(param_type='label', param_name='org.riotkit.domain', alert_days_before=1) \
                .main()

        finally:
            first.stop()
            second.stop()

        self.assertIn('Domain duckduckgo.com is OK', check[0])
        self.assertIn('Domain bing.com is OK', check[0])
        self.assertIn('Domain riseup.net is OK', check[0])
        self.assertTrue(check[1])

    def test_no_domains_found_will_result_in_error_status(self):
        check = TlsDockerNetworkCheck(param_type='label', param_name='invalid-label-name', alert_days_before=1) \
            .main()

        self.assertEqual('No any domains found, maybe the containers are not running?', check[0])
        self.assertFalse(check[1])


#!/usr/bin/python3

import os
import warnings
from unittest import TestCase
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

import infracheck.checks.smtp_credentials_check as smtpcheck


class FunctionalTestSmtpCredentials(TestCase):
    """
    SMTP functional tests using a real Postfix container
    ----------------------------------------------------
    Check container docs for detailed usage: https://github.com/riotkit-org/smtp-ext-relay
    """

    container: DockerContainer = None

    def tearDown(self):
        if self.container:
            self.container.stop()

    @staticmethod
    def _create_container() -> DockerContainer:
        return DockerContainer(image='quay.io/riotkit/smtp:v.1.1.0')\
            .with_command('bakunin.example.org durruti:durruti')\
            .with_bind_ports(25, 2525)

    def _start_container(self, container: DockerContainer):
        warnings.simplefilter("ignore")
        self.container = container
        self.container.start()
        wait_for_logs(self.container, 'daemon started')

    def test_connection_without_encryption_success_when_credentials_are_correct(self):
        self._start_container(self._create_container().with_env('SMTP_USE_TLS', 'false'))

        status, txt, err = smtpcheck.SMTPCheck().main("localhost", 2525, "durruti", "durruti", '', 15)

        self.assertTrue(status)
        self.assertEqual('Success', txt)

    def test_connection_without_encryption_failures_when_credentials_are_invalid(self):
        self._start_container(self._create_container().with_env('SMTP_USE_TLS', 'false'))

        status, txt, err = smtpcheck.SMTPCheck().main("localhost", 2525, "invalid", "invalid", '', 5)

        self.assertFalse(status)
        self.assertEqual('Authentication failed', txt)

    def test_connects_to_tls(self):
        self._start_container(
            self._create_container()
                .with_env('SMTP_USE_TLS', 'true')
                .with_env('SMTPD_TLS_CERT_FILE', '/keys/bakunin.example.org.crt')
                .with_env('SMTPD_TLS_KEY_FILE', '/keys/bakunin.example.org.key')
                .with_env('SMTP_TLS_CA_FILE', '/keys/cacert.pem')
                .with_env('ENABLE_DKIM', 'false')
                .with_volume_mapping(os.path.dirname(os.path.realpath(__file__)) + '/files/keys', '/keys', mode='ro')
        )

        status, txt, err = smtpcheck.SMTPCheck().main("127.0.0.1", 2525, "durruti", "durruti", 'starttls_self_signed', 5)
        self.assertTrue(status)

    def test_does_not_connect_to_starttls_if_self_signed_certificate_is_not_allowed(self):
        self._start_container(
            self._create_container()
                .with_env('SMTP_USE_TLS', 'true')
                .with_env('SMTPD_TLS_CERT_FILE', '/keys/bakunin.example.org.crt')
                .with_env('SMTPD_TLS_KEY_FILE', '/keys/bakunin.example.org.key')
                .with_env('SMTP_TLS_CA_FILE', '/keys/cacert.pem')
                .with_env('ENABLE_DKIM', 'false')
                .with_volume_mapping(os.path.dirname(os.path.realpath(__file__)) + '/files/keys', '/keys', mode='ro')
        )

        status, txt, err = smtpcheck.SMTPCheck().main("127.0.0.1", 2525, "durruti", "durruti", 'starttls', 5)
        self.assertIn('[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed', str(err))
        self.assertFalse(status)

    def test_connection_refused_when_invalid_port_entered(self):
        status, txt, err = smtpcheck.SMTPCheck().main("127.0.0.1", 2529, "durruti", "durruti", '', 2)
        self.assertFalse(status)
        self.assertEqual('Connection refused', txt)

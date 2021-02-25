#!/usr/bin/python3

import smtplib
from typing import Tuple
from unittest import TestCase
import infracheck.checks.smtp_credentials_check as smtpcheck
import unittest
import os


class TestSmtpCredentials(TestCase):
    @staticmethod
    def _create_mocked_method_raising(exception: Exception = None):
        def mock(a, b, c, d):
            if exception == None:
                pass
            else:
                raise exception
        check = smtpcheck.SMTPCheck()
        check._verify_credentials = mock
        return check

    @staticmethod
    def _run_mocked_check(testname: str, check: smtpcheck.SMTPCheck) -> Tuple[bool, str]:
        return check.main("host", 25, "username", "password")

    def test_expecting_success(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising()
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_success.__name__, check)
        assert (status, message) == (
            True, smtpcheck.Messages.SUCCESS.value)

    def test_expecting_SMTP_connection_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(
            smtplib.SMTPConnectError(0, ''))
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_SMTP_connection_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.SMTP_CONNECTION_ERROR.value)

    def test_expecting_general_connection_refused_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(ConnectionRefusedError())
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_general_connection_refused_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.CONNECTION_REFUSED_ERROR.value)

    def test_expecting_SMTP_helo_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(
            smtplib.SMTPHeloError(0, ''))
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_SMTP_helo_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.HELO_OR_EHLO_ERROR.value)

    def test_expecting_SMTP_server_disconnected_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(
            smtplib.SMTPServerDisconnected())
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_SMTP_server_disconnected_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.DISCONNECTION_ERROR.value)

    def test_expecting_SMTP_authentication_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(
            smtplib.SMTPAuthenticationError(0, ''))
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_SMTP_authentication_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.AUTHENTICATION_ERROR.value)

    def test_expecting_general_SMTP_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(smtplib.SMTPException())
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_general_SMTP_error.__name__, check)
        assert (status, message) == (
            False, smtpcheck.Messages.UNKNOWN_SMTP_ERROR.value)

    def test_expecting_general_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(Exception())
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_general_error.__name__, check)
        assert (status, message) == (False, smtpcheck.Messages.UNKNOWN_ERROR.value)
    
    def test_expecting_auth_command_not_supported_error(self) -> None:
        check = TestSmtpCredentials._create_mocked_method_raising(smtplib.SMTPNotSupportedError())
        status, message = TestSmtpCredentials._run_mocked_check(
            self.test_expecting_auth_command_not_supported_error.__name__, check)

        self.assertEqual(
            (status, message),
            (False, smtpcheck.Messages.AUTH_METHOD_NOT_SUPPORTED_BY_SERVER.value)
        )

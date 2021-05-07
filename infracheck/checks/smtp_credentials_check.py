#!/usr/bin/python3
"""
<sphinx>
smtp_credentials_check.py
-------------------------

Verifies connection, TLS certificate and credentials to a SMTP server by doing a ping + authorization try.

Parameters:

- smtp_host (example: bakunin.example.org)
- smtp_port (example: 25)
- smtp_user (example: noreply@example.org)
- smtp_password (example: bakunin-1936)
- smtp_encryption (example: starttls. Values: "", "ssl", "starttls")
- smtp_timeout (default: 30, unit: seconds)
</sphinx>
"""

import enum
import os
import smtplib
import ssl
import socket
import sys
from typing import Tuple, Optional


class Messages(enum.Enum):
    SUCCESS = 'Success'
    SMTP_CONNECTION_ERROR = 'Error connecting to the SMTP server'
    SMTP_HELO_OR_EHLO_ERROR = 'HELO or EHLO error'
    SMTP_AUTHENTICATION_ERROR = 'Authentication failed'
    SMTP_DISCONNECTION_ERROR = 'Server is disconnected'
    GENERAL_ERROR = 'General error'
    GENERAL_SMTP_ERROR = 'General SMTP error'
    SOCKET_TIMEOUT = 'Connection timeout'
    CONNECTION_REFUSED_ERROR = 'Connection refused'
    SMTP_AUTH_METHOD_NOT_SUPPORTED_BY_SERVER = 'AUTH command not supported by the server'


class EnvKeys(enum.Enum):
    HOST = 'SMTP_HOST'
    PORT = 'SMTP_PORT'
    USERNAME = 'SMTP_USER'
    PASSWORD = 'SMTP_PASSWORD'
    ENCRYPTION = 'SMTP_ENCRYPTION'
    TIMEOUT = 'SMTP_TIMEOUT'
    DEBUG = 'SMTP_DEBUG'


class Encryption(enum.Enum):
    ENC_NONE = ''
    ENC_SSL = 'ssl'
    ENC_STARTTLS = 'starttls'
    ENC_STARTTLS_SELF_SIGNED = 'starttls_self_signed'


class SMTPCheck(object):
    def main(self, host: str, port: int, username: str, password: str, encryption: str,
             timeout: int, debug: bool = False) \
            -> Tuple[bool, str, Optional[Exception]]:

        try:
            self._verify_connection(host, port, username, password, encryption, timeout, debug)
            return True, Messages.SUCCESS.value, None

        except smtplib.SMTPConnectError as exc:
            return False, Messages.SMTP_CONNECTION_ERROR.value, exc

        except smtplib.SMTPHeloError as exc:
            return False, Messages.SMTP_HELO_OR_EHLO_ERROR.value, exc

        except smtplib.SMTPAuthenticationError as exc:
            return False, Messages.SMTP_AUTHENTICATION_ERROR.value, exc

        except smtplib.SMTPServerDisconnected as exc:
            return False, Messages.SMTP_DISCONNECTION_ERROR.value, exc

        except smtplib.SMTPNotSupportedError as exc:
            return False, Messages.SMTP_AUTH_METHOD_NOT_SUPPORTED_BY_SERVER.value, exc

        except smtplib.SMTPException as exc:
            return False, Messages.GENERAL_SMTP_ERROR.value, exc

        except socket.timeout as exc:
            return False, Messages.SOCKET_TIMEOUT.value, exc

        except ConnectionRefusedError as exc:
            return False, Messages.CONNECTION_REFUSED_ERROR.value, exc

        except Exception as exc:
            return False, Messages.GENERAL_ERROR.value, exc

    @staticmethod
    def _verify_connection(host: str, port: int, username: str, password: str,
                           encryption: str, timeout: int, debug: bool):

        connection = smtplib.SMTP_SSL(host, port, timeout=timeout) if encryption == Encryption.ENC_SSL.value else \
            smtplib.SMTP(host, port, timeout=timeout)

        connection.set_debuglevel(1 if debug else 0)

        if encryption == Encryption.ENC_STARTTLS.value:
            connection.starttls(context=ssl.create_default_context())

        elif encryption == Encryption.ENC_STARTTLS_SELF_SIGNED.value:
            connection.starttls(context=ssl._create_unverified_context())

        if username and password:
            connection.login(username, password)

        connection.close()


if __name__ == '__main__':
    inputs = {
        EnvKeys.HOST.value: os.getenv(EnvKeys.HOST.value),
        EnvKeys.PORT.value: os.getenv(EnvKeys.PORT.value),
        EnvKeys.USERNAME.value: os.getenv(EnvKeys.USERNAME.value),
        EnvKeys.PASSWORD.value: os.getenv(EnvKeys.PASSWORD.value),
        EnvKeys.ENCRYPTION.value: os.getenv(EnvKeys.ENCRYPTION.value, 'starttls'),
        EnvKeys.TIMEOUT.value: os.getenv(EnvKeys.TIMEOUT.value, 30),
        EnvKeys.DEBUG.value: os.getenv(EnvKeys.DEBUG.value, False)
    }

    for key in inputs:
        if inputs[key] is None:
            print('Missing environment variable: {}'.format(key))
            sys.exit(1)

    app = SMTPCheck()
    is_success, message, exception = app.main(
        inputs[EnvKeys.HOST.value],
        int(inputs[EnvKeys.PORT.value]),
        inputs[EnvKeys.USERNAME.value],
        inputs[EnvKeys.PASSWORD.value],
        inputs[EnvKeys.ENCRYPTION.value],
        int(inputs[EnvKeys.TIMEOUT.value]),
        bool(inputs[EnvKeys.DEBUG.value])
    )

    print(('Error: {}'.format(message)) if exception else message)

    if exception is not None:
        print('Exception:', exception)

    sys.exit(0 if is_success else 1)

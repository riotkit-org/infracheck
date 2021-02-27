#!/usr/bin/python3
"""
<sphinx>
Verifies SMTP credentials by using smtplib module to log in at the server.
Arguments are provided via environmental variables:

SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
</sphinx>
"""

import enum
import os
import smtplib
import sys
from typing import Tuple


class Messages(enum.Enum):
    SUCCESS = 'Success'
    SMTP_CONNECTION_ERROR = 'Error connecting to the SMTP server'
    SMTP_HELO_OR_EHLO_ERROR = 'HELO or EHLO error'
    SMTP_AUTHENTICATION_ERROR = 'Authentication failed'
    SMTP_DISCONNECTION_ERROR = 'Server is disconnected'
    GENERAL_ERROR = 'General error'
    GENERAL_SMTP_ERROR = 'General SMTP error'
    CONNECTION_REFUSED_ERROR = 'Connection refused'
    SMTP_AUTH_METHOD_NOT_SUPPORTED_BY_SERVER = 'AUTH command not supported by the server'


class EnvKeys(enum.Enum):
    HOST = 'SMTP_HOST'
    PORT = 'SMTP_PORT'
    USERNAME = 'SMTP_USER'
    PASSWORD = 'SMTP_PASSWORD'


class SMTPCheck():
    def main(self, host: str, port: int, username: str, password: str) -> Tuple[int, str, OSError]:
        try:
            self._verify_credentials(host, port, username, password)
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
        except ConnectionRefusedError as exc:
            return False, Messages.CONNECTION_REFUSED_ERROR.value, exc
        except Exception as exc:
            return False, Messages.GENERAL_ERROR.value, exc

    def _verify_credentials(self, host, port, username, password):
        connection = smtplib.SMTP_SSL(host, port)
        connection.set_debuglevel(1)
        connection.login(username, password)
        connection.close()


if __name__ == '__main__':
    inputs = {
        EnvKeys.HOST.value: os.getenv(EnvKeys.HOST.value),
        EnvKeys.PORT.value: os.getenv(EnvKeys.PORT.value),
        EnvKeys.USERNAME.value: os.getenv(EnvKeys.USERNAME.value),
        EnvKeys.PASSWORD.value: os.getenv(EnvKeys.PASSWORD.value)
    }

    for key in inputs:
        if inputs[key] is None:
            print('Missing environment variable: {}'.format(key))
            sys.exit(1)

    app = SMTPCheck()
    isSuccess, message, exception = app.main(
        inputs[EnvKeys.HOST.value],
        int(inputs[EnvKeys.PORT.value]),
        inputs[EnvKeys.USERNAME.value],
        inputs[EnvKeys.PASSWORD.value]
    )

    print(message)
    if(exception is not None): print(exception)
    sys.exit(0 if isSuccess else 1)

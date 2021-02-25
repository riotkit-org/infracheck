#!/usr/bin/python3
"""
<sphinx>
Verifies SMTP credentials by using smtplib module to log in at the server.
Arguments are provided via environmental variables:
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
"""

import smtplib
import os
import enum
import sys
from typing import Tuple


class Messages(enum.Enum):
    SUCCESS = 'Success'
    SMTP_CONNECTION_ERROR = 'Error connecting to the SMTP server'
    HELO_OR_EHLO_ERROR = 'HELO or EHLO error'
    AUTHENTICATION_ERROR = 'Authentication failed'
    DISCONNECTION_ERROR = 'Server is disconnected'
    UNKNOWN_ERROR = 'Unknown error'
    UNKNOWN_SMTP_ERROR = 'Unknown SMTP error'
    CONNECTION_REFUSED_ERROR = 'Connection refused'
    AUTH_METHOD_NOT_SUPPORTED_BY_SERVER = 'AUTH command not supported by the server'


class EnvKeys(enum.Enum):
    HOST = 'SMTP_HOST'
    PORT = 'SMTP_PORT'
    USERNAME = 'SMTP_USER'
    PASSWORD = 'SMTP_PASSWORD'


class SMTPCheck():
    def main(self, host: str, port: int, username: str, password: str) -> Tuple[int, int]:
        try:
            self._verify_credentials(host, port, username, password)
            return True, Messages.SUCCESS.value,
        except smtplib.SMTPConnectError:
            return False, Messages.SMTP_CONNECTION_ERROR.value
        except smtplib.SMTPHeloError:
            return False, Messages.HELO_OR_EHLO_ERROR.value
        except smtplib.SMTPAuthenticationError:
            return False, Messages.AUTHENTICATION_ERROR.value
        except smtplib.SMTPServerDisconnected:
            return False, Messages.DISCONNECTION_ERROR.value
        except smtplib.SMTPNotSupportedError:
            return False, Messages.AUTH_METHOD_NOT_SUPPORTED_BY_SERVER.value
        except smtplib.SMTPException:
            return False, Messages.UNKNOWN_SMTP_ERROR.value
        except ConnectionRefusedError:
            return False, Messages.CONNECTION_REFUSED_ERROR.value
        except Exception:
            return False, Messages.UNKNOWN_ERROR.value

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
    isSuccess, message = app.main(
        inputs[EnvKeys.HOST.value],
        int(inputs[EnvKeys.PORT.value]),
        inputs[EnvKeys.USERNAME.value],
        inputs[EnvKeys.PASSWORD.value]
    )

    print(message)
    sys.exit(0 if isSuccess else 1)

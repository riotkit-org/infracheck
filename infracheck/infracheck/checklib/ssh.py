
import subprocess
import os
from typing import Union, Tuple


class SSH:
    user: str
    port: int
    host: str
    ssh_opts: str
    ssh_bin: str
    timeout: int
    sshpass_bin: str
    known_hosts_file: str

    def __init__(self, user: str, port: int, host: str, ssh_opts: str, private_key: str,
                 ssh_bin: str, password: str, timeout: int, sshpass_bin: str, known_hosts_file: str):
        self.user = user
        self.port = port
        self.host = host
        self.ssh_opts = ssh_opts
        self.ssh_bin = ssh_bin
        self.password = password
        self.timeout = timeout
        self.sshpass_bin = sshpass_bin
        self.known_hosts_file = os.path.expanduser(known_hosts_file if known_hosts_file else '~/.ssh/known_hosts')

        if self.known_hosts_file:
            self.ssh_opts += ' -o UserKnownHostsFile=' + self.known_hosts_file

        if private_key:
            self.ssh_opts += ' -i %s ' % private_key

    def execute(self, remote_command: Union[str, list]) -> Tuple[str, int]:
        self._make_sure_host_is_known()

        local_command = [self.ssh_bin]

        if self.password:
            local_command = [self.sshpass_bin, '-p', self.password] + local_command

        if self.ssh_opts:
            local_command += self.ssh_opts.strip().split(' ')

        local_command += [
            '-p', str(self.port),
            self.user + '@' + self.host
        ]

        if type(remote_command) == str:
            local_command.append(remote_command)
        else:
            local_command += remote_command

        try:
            out = subprocess.check_output(local_command, stderr=subprocess.STDOUT, timeout=self.timeout).decode('utf-8')
            exit_code = 0
        except subprocess.CalledProcessError as e:
            out = e.output.decode('utf-8')
            exit_code = e.returncode

        return out, exit_code

    def _make_sure_host_is_known(self):
        pattern = self.host if self.port == 22 else '[' + self.host + ']:' + str(self.port)
        os.system('mkdir -p $(dirname %s); touch %s' % (self.known_hosts_file, self.known_hosts_file))

        with open(self.known_hosts_file, 'rb') as f:
            current_content = f.read().decode('utf-8')

            if pattern not in current_content:
                self._add_host_to_known_hosts()

    def _add_host_to_known_hosts(self):
        subprocess.call(
            'ssh-keyscan -p %i %s >> %s' % (self.port, self.host, self.known_hosts_file), shell=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

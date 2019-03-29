
import os
import posix


class Repository:
    checks_dirs = []      # type: list
    configured_dirs = []  # type: list

    def __init__(self, project_dirs: list):
        for path in project_dirs:
            self.checks_dirs.append(path + '/checks')
            self.configured_dirs.append(path + '/configured')

    def get_configured_checks(self, with_disabled=False):
        found = []

        for path in self.configured_dirs:
            if not os.path.isdir(path):
                continue

            configurations = os.scandir(path)

            for entry in configurations:
                if not with_disabled and not entry.name.endswith('.json'):
                    continue
                elif with_disabled and not (entry.name.endswith('.disabled') or entry.name.endswith('.json')):
                    continue

                found.append(os.path.splitext(entry.name)[0].replace('.json', ''))

        return list(set(found))

    def get_available_checks(self):
        results = []

        for path in self.checks_dirs:
            available_checks = os.scandir(path)

            def map_checks_to_name(check: posix.DirEntry):
                return str(check.name)

            results += map(map_checks_to_name, available_checks)

        return list(set(results))

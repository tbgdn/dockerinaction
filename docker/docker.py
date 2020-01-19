import subprocess


class Docker:
    def __init__(self, label='docker'):
        self.label = label

    @staticmethod
    def print_command_id(command, id):
        print('{0} with id: {1}'.format(command, id))

    def create(self, args):
        return self.docker(['create', '--label', self.label] + args)

    def run(self, args):
        return self.docker(['run', '--label', self.label] + args)

    def start(self, id):
        return self.docker(['start', id])

    def docker(self, args):
        return self.run_command(['docker'] + args)

    def run_command(self, args):
        print('[Docker] {0}'.format(' '.join(args)))
        result = subprocess.run(
            args,
            capture_output=True,
            shell=True,
            encoding='utf-8')
        if (result.returncode):
            print(result.stderr)
            print(result.stdout)
            result.check_returncode()

        res = result.stdout
        return res.strip().strip("\"")

    def cleanup(self):
        print('[Docker] Cleaning up...')
        containerIds = self.docker(['ps', '-a', '--filter', 'label=' + self.label, '-q'])
        for id in containerIds.split('\n'):
            id = self.docker(['stop', id])
            logs = self.docker(['logs', id])
            print('[Docker] Logging for {0}\n{1}'.format(id, logs))
            id = self.docker(['rm', id])
            print('===')

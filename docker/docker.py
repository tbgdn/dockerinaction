import subprocess


class Docker(object):
    def __init__(self, label='docker'):
        self.label = label

    @staticmethod
    def print_command_id(command, id):
        print('{0} with id: {1}'.format(command, id))

    def docker_create(self, args):
        return self.docker(['create', '--label', self.label] + args)

    def docker_run(self, args):
        return self.docker(['run', '--label', self.label] + args)

    def docker_start(self, args):
        return self.docker(['start'] + args)

    def docker(self, args):
        return self.run_command(['docker'] + args)

    def run_command(self, args):
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
        print('Cleaning up Docker...')
        containerIds = self.docker(['ps', '-a', '--filter', 'label=' + self.label, '-q'])
        for id in containerIds.split('\n'):
            self.print_command_id('stopping', id)
            id = self.docker(['stop', id])
            logs = self.docker(['logs', id])
            print('Logging for {0}\n{1}'.format(id, logs))
            self.print_command_id('---\nremoving', id)
            id = self.docker(['rm', id])
            self.print_command_id('removed', id)
            print('===')

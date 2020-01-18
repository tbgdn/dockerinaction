import cmd, sys


class Repl(cmd.Cmd):
    intro = 'Wordpress commander'
    prompt = '[wp]'

    def __init__(self, docker):
        super().__init__()
        self.docker = docker

    def do_stop(self):
        self.close()

    def do_exit(self):
        self.close()

    def close(self):
        if self.docker:
            self.docker.cleanup()
        sys.exit(0)

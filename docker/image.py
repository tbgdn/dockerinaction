from .docker import Docker

class Image:
    def __init__(self, docker: Docker):
        self.tags = []
        self.docker = docker

    def build(self, args):
        if (len(args) > 0):
            self.tags = self.tags + [args[0]]
        self.docker.docker(['image', 'build', '-t'] + args)

    def cleanup(self):
        for image_tag in self.tags:
            print(f'Removing image: {image_tag}')
            self.docker.docker(['image', 'rm', '-f', image_tag])

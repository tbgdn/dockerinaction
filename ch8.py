import os
from docker import Docker
from docker import Repl
from docker import Image

docker = Docker('version')
image = Image(docker)

try:
    version=0.6
    image_id = image.build([f'dockerinaction/mailer-base:{version}', '-f', 'mailer-base.df', '--build-arg', f'VERSION={version}', './resources/ch8/mailer-base'])
    print(f'Finished creating docker image: {image_id}')
except Exception as err:
    print(f'Error running arg_version example\n{err}')
    image.cleanup()
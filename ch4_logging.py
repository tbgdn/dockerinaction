import os
from docker import Docker
from docker import Repl

docker = Docker('logging-example')
repl = Repl(docker)

try:
    volume_name = 'logging-example'
    docker.volumeCreate(['--driver', 'local', volume_name])
    docker.run(['--name', 'plath', '-d', '--mount', f'type=volume,src={volume_name},dst=/data', 'dockerinaction/ch4_writer_a'])
    some_data = docker.run(['--rm', '--mount', f'type=volume,src={volume_name},dst=/data', 'alpine:latest', 'head', '/data/logA'])
    print(f'Did we get data?\n{some_data}')
    log_a_path = docker.volumeInspect(['--format', '"{{json .Mountpoint}}"', volume_name])
    print(f'Logging file source path:\n{log_a_path}')
    repl.cmdloop('Logging...')
except Exception as err:
    print(f'Error running logging example\n{err}')
    docker.cleanup()
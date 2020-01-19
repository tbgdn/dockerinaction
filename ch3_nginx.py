import os
from docker import Docker
from docker import Repl

config_src = os.path.abspath('resources\\ch3_nginx.conf')
config_dest = '/etc/nginx/conf.d/default.conf'

log_src = os.path.abspath('resources\\ch3_nginx.log')
log_dest = '/var/log/nginx/custom.host.access.log'

docker = Docker('dia-nginx')
repl = Repl(docker)

try:
    docker.run(
        ['-d', '--name', 'diaweb', '--mount', f'type=bind,src={config_src},dst={config_dest},readonly=true', '--mount',
         f'type=bind,src={log_src},dst={log_dest}', '-p', '80:80', 'nginx:latest'])
    repl.cmdloop('Running nginx...')
except Exception as err:
    print('Error running nginx:\n{0}'.format(err))
    docker.cleanup()

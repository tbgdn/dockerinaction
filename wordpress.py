from docker import Docker
from docker import Repl

docker = Docker('wordpress')

try:
    db_cid = docker.create(['-e', 'MYSQL_ROOT_PASSWORD=ch2demo', 'mysql:5.7'])
    docker.start(db_cid)
    mailer_cid = docker.create(['dockerinaction/ch2_mailer'])
    docker.start(mailer_cid)
    wp_cid = docker.create(
        ['--link', '{0}:mysql'.format(db_cid), '-p', '8080:80', '--read-only', '-v', '/run/apache2/', '--tmpfs', '/tmp',
         'wordpress:5.0.0-php7.2-apache'])
    docker.start(wp_cid)
    agent_cid = docker.create(
        ['--link', '{0}:insideweb'.format(wp_cid), '--link', '{0}:insidemailer'.format(mailer_cid),
         'dockerinaction/ch2_agent'])
    docker.start(agent_cid)
    cmd = Repl(docker)
    cmd.cmdloop()

except Exception as err:
    print('Error creating wordpress:\n{0}', err)
    docker.cleanup()

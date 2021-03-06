import subprocess
from time import sleep
from docker import Docker


def runChapter(d):
    mailer_cid = d.run(['-d', 'dockerinaction/ch2_mailer'])
    Docker.print_command_id('running mailer', mailer_cid)
    webCid = d.create(['nginx'])
    d.print_command_id('created web', webCid)
    agent_cid = d.create(
        ['--link', '%s:insideweb' % webCid, '--link', '%s:insidemailer' % mailer_cid, 'dockerinaction/ch2_agent'])
    d.print_command_id('created agent', agent_cid)
    webRid = d.start(webCid)
    d.print_command_id('running web', webRid)
    agentRid = d.start(agent_cid)
    d.print_command_id('running agent', agentRid)


docker = Docker('dockerinaction')
try:
    timeout = 1
    runChapter(docker)
    print('Running for {0}s'.format(timeout))
    sleep(timeout)
    docker.cleanup()
except subprocess.CalledProcessError as err:
    print('Some error was thrown while executing docker command:\n{0}'.format(err))
    docker.cleanup()

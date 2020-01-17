import subprocess
from time import sleep

def printCommandId(command, id):
    print('{0} with id: {1}'.format(command, id))

def dockerCreate(args):
    return docker(['create', '--label', 'dockerinaction'] + args)

def dockerRun(args):
    return docker(['run', '--label', 'dockerinaction'] + args)

def dockerStart(args):
    return docker(['start'] + args)

def docker(args):
    return runCommand(['docker'] + args)

def runCommand(args):
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

def removeAllContainers():
    print('Cleaning up Docker...')
    containerIds = docker(['ps', '-a', '--filter', 'label=dockerinaction', '-q'])
    for id in containerIds.split('\n'):
        printCommandId('stopping', id)
        id = docker(['stop', id])
        logs = docker(['logs', id])
        print('Logging for {0}\n{1}'.format(id, logs))
        printCommandId('---\nremoving', id)
        id = docker(['rm', id])
        printCommandId('removed', id)
        print('===')

def runChapter():
    mailerCid = dockerRun(['-d', 'dockerinaction/ch2_mailer'])
    printCommandId('running mailer', mailerCid)
    webCid = dockerCreate(['nginx'])
    printCommandId('created web', webCid)
    agentCid = dockerCreate([ '--link', '%s:insideweb' % webCid, '--link', '%s:insidemailer' % mailerCid, 'dockerinaction/ch2_agent'])
    printCommandId('created agent', agentCid)
    webRid = dockerStart([webCid])
    printCommandId('running web', webRid)
    agentRid = dockerStart([agentCid])
    printCommandId('running agent', agentRid)

try:
    timeout = 1
    runChapter()
    print('Running for {0}s'.format(timeout))
    sleep(timeout)
    removeAllContainers()
except subprocess.CalledProcessError as err:
    print('Some error was thrown while executing docker command:\n{0}'.format(err))
    removeAllContainers()
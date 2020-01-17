import subprocess
from time import sleep

def printCommandId(command, id):
    print('{0} with id: {1}'.format(command, id))

def dockerRun(args):
    return docker(['run'] + args)

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
    containerIds = docker(['ps', '-a', '-q'])
    for id in containerIds.split('\n'):
        printCommandId('stopping', id)
        id = docker(['stop', id])
        printCommandId('removing', id)
        id = docker(['rm', id])
        printCommandId('removed', id)

def runChapter():
    mailerCid = dockerRun(['-d', 'dockerinaction/ch2_mailer'])
    print('running %s' % mailerCid)
    webCid = docker(['create', 'nginx'])
    printCommandId('created', webCid)
    agentCid = docker(['create', '--link', '%s:insideweb' % webCid, '--link', '%s:insidemailer' % mailerCid, 'dockerinaction/ch2_agent'])
    print('created %s' % agentCid)
    webRid = dockerStart([webCid])
    agentRid = dockerStart([agentCid])
    printCommandId('running', webRid)
    print('running %s' % agentRid)

try:
    timeout = 10
    runChapter()
    print('Running for {0}s'.format(timeout))
    sleep(timeout)
    removeAllContainers()
except subprocess.CalledProcessError as err:
    print('Some error was thrown while executing docker command:\n{0}'.format(err))
    removeAllContainers()